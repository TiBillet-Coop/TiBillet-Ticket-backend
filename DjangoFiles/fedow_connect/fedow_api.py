import json
import logging
from datetime import datetime
from uuid import UUID

import requests
from django.conf import settings

from AuthBillet.models import RsaKey, TibilletUser, Wallet
from BaseBillet.models import Configuration
from fedow_connect.models import FedowConfig
from fedow_connect.utils import sign_message, data_to_b64, verify_signature
from fedow_connect.validators import WalletValidator

logger = logging.getLogger(__name__)


### GENERIC GET AND POST ###
def _post(fedow_config: FedowConfig = None,
          user: TibilletUser = None,
          data: dict = None,
          path: str = None,
          apikey: str = None):
    fedow_domain = fedow_config.fedow_domain()
    wallet_uuid: str = f"{user.wallet.uuid}" if user.wallet else ""

    # Pour la création, on prend la clé api de Root. On rempli apikey
    # Si vide, on prend la clé du lieu du tenant
    if apikey is None:
        apikey = fedow_config.fedow_place_admin_apikey

    # Signature de la requete
    private_key = user.get_private_key()
    signature = sign_message(
        data_to_b64(data),
        private_key,
    ).decode('utf-8')

    # Ici, on s'autovérifie :
    # Assert volontaire. Si non effectué en prod, ce n'est pas grave.
    # logger.debug("_post verify_signature start")
    assert verify_signature(user.get_public_key(),
                            data_to_b64(data),
                            signature)

    session = requests.Session()
    request_fedow = session.post(
        f"https://{fedow_domain}/{path}/",
        headers={
            "Wallet": f"{wallet_uuid}",
            "Date": f"{datetime.now().isoformat()}",
            "Authorization": f"Api-Key {apikey}",
            "Signature": f"{signature}",
            "Content-type": "application/json",
        },
        data=json.dumps(data),
        verify=bool(not settings.DEBUG),
    )

    # TODO: Vérifier la signature de FEDOW avec root_config.fedow_primary_pub_pem

    session.close()
    return request_fedow


def _get(fedow_config: FedowConfig = None,
         user: TibilletUser = None,
         path: str = None,
         apikey: str = None):

    fedow_domain = fedow_config.fedow_domain()

    # Pour la création, on prend la clé api de Root. On rempli apikey
    # Si vide, on prend la clé du lieu du tenant
    if apikey is None:
        apikey = fedow_config.fedow_place_admin_apikey

    # Signature de la requete : on signe le path
    private_key = user.get_private_key()
    # Signature de la requete : on signe la clé

    # On signe le message
    now = f"{datetime.now().isoformat()}"
    message = f"{user.wallet.uuid}:{now}"
    signature = sign_message(
        message.encode('utf8'),
        private_key,
    ).decode('utf-8')

    # Ici, on s'autovérifie :
    # Assert volontaire. Si non effectué en prod, ce n'est pas grave.
    assert verify_signature(user.get_public_key(),
                            message.encode('utf8'),
                            signature)

    session = requests.Session()
    request_fedow = session.get(
        f"https://{fedow_domain}/{path}/",
        headers={
            "Date": f"{now}",
            'Authorization': f'Api-Key {apikey}',
            "Wallet": f"{user.wallet.uuid}",
            "Signature": f"{signature}",
        },
        verify=bool(not settings.DEBUG),
    )
    session.close()
    # TODO: Vérifier la signature de FEDOW
    return request_fedow


class WalletFedow():
    def __init__(self, fedow_config):
        self.fedow_config: FedowConfig = fedow_config
        if not fedow_config:
            self.fedow_config = FedowConfig.get_solo()

    def retrieve_by_signature(self, user):
        response_link = _get(
            self.fedow_config,
            user=user,
            path=f'wallet/retrieve_by_signature'
        )

        if not response_link.status_code == 200:
            logger.error(f"retrieve_by_signature ERRORS : {response_link.status_code}")
            raise Exception(f"retrieve_by_signature ERRORS : {response_link.status_code}")

        wallet_serialized = WalletValidator(data=response_link.json())
        if wallet_serialized.is_valid():
            return wallet_serialized
        else:
            logger.error(f"retrieve_by_signature wallet_serialized ERRORS : {wallet_serialized.errors}")
            raise Exception(f"retrieve_by_signature wallet_serialized ERRORS : {wallet_serialized.errors}")


    def get_or_create(self, user: TibilletUser):
        email = user.email
        response_link = _post(self.fedow_config, user=user, path='wallet/get_or_create', data={
            "email": email,
            "public_pem": user.get_public_pem(),
        })
        if response_link.status_code in [200, 201]:
            # Création du wallet dans la base de donnée
            if not user.wallet:
                user.wallet, created = Wallet.objects.get_or_create(uuid=UUID(response_link.json()))
                user.save()
            elif user.wallet.uuid != UUID(response_link.json()):
                raise Exception("Wallet and member mismatch")

            created = False if response_link.status_code == 200 else True
            return user.wallet, created

        raise Exception(f"Wallet FedowAPI create_from_email response : {response_link.status_code}")


    def get_federated_token_refill_checkout(self, user: TibilletUser):
        response_checkout = _get(
            self.fedow_config,
            user=user,
            path=f'wallet/get_federated_token_refill_checkout'
        )

        if response_checkout.status_code != 202:
            logger.error(response_checkout.json())
            raise Exception(response_checkout.json())

        stripe_checkout_url = response_checkout.json()
        return stripe_checkout_url


class PlaceFedow():
    def __init__(self, fedow_config):
        self.fedow_config: FedowConfig = fedow_config
        if not fedow_config:
            self.fedow_config = FedowConfig.get_solo()

    def create(self, admin: TibilletUser = None, place_name=None):
        if any([
            self.fedow_config.fedow_place_uuid,
            self.fedow_config.fedow_place_wallet_uuid,
            self.fedow_config.fedow_place_admin_apikey,
        ]):
            raise Exception("Place already created")

        if place_name is None:
            tenant_config = Configuration.get_solo()
            place_name = tenant_config.organisation

        # Pour la création, on prend la clé api de Root
        apikey = self.fedow_config.get_fedow_create_place_apikey()
        data = {
            'place_name': place_name,
            'admin_email': admin.email,
            'admin_pub_pem': admin.get_public_pem(),
        }

        new_place = _post(fedow_config=self.fedow_config,
                          user=admin,
                          path='place',
                          data=data, apikey=apikey)
        new_place_data = new_place.json()
        self.fedow_config.fedow_place_uuid = new_place_data['uuid']
        self.fedow_config.fedow_place_wallet_uuid = new_place_data['wallet']
        self.fedow_config.fedow_place_admin_apikey = new_place_data['key']
        self.fedow_config.save()


# from fedow_connect.fedow_api import FedowAPI
class FedowAPI():
    def __init__(self, fedow_config: FedowConfig = None):
        self.fedow_config = fedow_config
        if fedow_config is None:
            self.fedow_config = FedowConfig.get_solo()

        self.wallet = WalletFedow(self.fedow_config)
        self.place = PlaceFedow(self.fedow_config)

    def handshake(self):
        pass
