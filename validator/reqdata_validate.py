import yaml
import json
from error.yaml_exception import FormatError
from drivers import SERVICE_REGISTERY_TOP_KEY, SERVICE_DRIVERS


top_keys = ["apiVersion", "kind", "metadata"]

kinds = ["VpcSandBox", "ServiceRegister", "ServicePublisher", "Namespace"]


def basic_validate(req_data):

    try:

        for key in top_keys:

            if key not in req_data.keys():

                raise FormatError("You must provide %s!" % key)

        if req_data.get("kind") not in kinds:

            raise FormatError("%s not belong to vulcanus-engine!" % req_data.get("kind"))

        if req_data.get("apiVersion") != "v1":

            raise FormatError("Only v1 was supported now!")


    except FormatError as e:

        raise

    except Exception as e:

        raise


def namespace_validate(req_data):

    try:

        if not req_data.get("kind") == "Namespace":

            raise FormatError("Kind must specified to Namespace!")

        if not req_data.get("metadata").get("name"):

            raise FormatError("Namespace must specified name!")

    except FormatError as e:

        print e.err

        raise

    except Exception as e:

        raise


def srvs_register_validate(req_data):

    try:

        if not req_data.get("kind") == "ServiceRegister":

            raise FormatError("Kind must specified to ServiceRegister!")

        if not req_data.get("metadata").get("name"):

            raise FormatError("You must specified the service name in metadata block!")

        if not req_data.get("spec"):

            raise FormatError("ServiceRegister must specified the spec block!")

        for key in SERVICE_REGISTERY_TOP_KEY:

            if key not in req_data.get("spec").keys():

                raise FormatError("%s must specified the spec block!" % key)

        if req_data.get("spec").get("input").get("Driver"):

            if req_data.get("spec").get("input").get("Driver") not in SERVICE_DRIVERS:

                raise FormatError("%s is not supported!" % req_data.get("spec").get("input").get("Driver"))

    except FormatError as e:

        print e.err
        raise

if __name__ == '__main__':

    basic_validate(yaml.load(file("/Users/scott/PycharmProjects/vulcanus-engine/yaml_file_template/namespace.yaml")))
    namespace_validate(yaml.load(file("/Users/scott/PycharmProjects/vulcanus-engine/yaml_file_template/namespace.yaml")))




