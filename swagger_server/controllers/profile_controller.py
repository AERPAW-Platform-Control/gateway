import connexion
import six
from flask import abort
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server import util
from . import emulab
import json
import os
import logging

logger = logging.getLogger(__name__)


def create_profile(body):  # noqa: E501
    """create profile

    Create Profile # noqa: E501

    :param body: Profile Object
    :type body: dict | bytes

    :rtype: ApiResponse
    """
    if connexion.request.is_json:
        req = Profile.from_dict(connexion.request.get_json())  # noqa: E501

    if req.creator is None:
        req.creator = emulab.EMULAB_EXPERIMENT_USER
    if req.project is None:
        req.project = emulab.EMULAB_PROJ

    xmlfile = emulab.write_profile_xml(req.project, req.name, req.script, req.repourl)
    xmlpath = emulab.send_file(xmlfile)

    emulab_cmd = '{} sudo -u {} manage_profile create {}'.format(
                emulab.SSH_BOSS, req.creator, xmlpath)
    emulab.send_request(emulab_cmd)

    # clean up the temporary files
    os.unlink(xmlfile)
    emulab_cmd = '{} sudo rm {}'.format(emulab.SSH_BOSS, xmlpath)
    emulab.send_request(emulab_cmd)

    response = ApiResponse(code=0,
                           output="Please use getProfile to check whether success or fail")
    return response


def delete_profile(name, username=None, project=None):  # noqa: E501
    """delete profile

    delete profile # noqa: E501

    :param name: name of profile to delete
    :type name: str
    :param username: username for the request
    :type username: str
    :param project: project name
    :type project: str

    :rtype: None
    """

    if username is None:
        username = emulab.EMULAB_EXPERIMENT_USER
    if project is None:
        project = emulab.EMULAB_PROJ

    emulab_cmd = '{} sudo -u {} manage_profile delete {},{}'.format(
        emulab.SSH_BOSS, username, project, name)
    emulab.send_request(emulab_cmd)
    response = ApiResponse(code=0,
                           output="Please use getProfile to check whether success or fail")
    return response


def get_profiles(username=None):  # noqa: E501
    """get profiles under user

    get profiles under user # noqa: E501

    :param username: creator of the profile
    :type username: str

    :rtype: List[Profile]
    """
    if username is None:
        username = emulab.EMULAB_EXPERIMENT_USER
        logger.info('user default user!')

    emulab_cmd = '{} sudo python /root/aerpaw/querydb.py {} list_profiles'.format(
                    emulab.SSH_BOSS, username)
    emulab_stdout = emulab.send_request(emulab_cmd)
    profiles = []
    if emulab_stdout:
        results = json.loads(emulab_stdout)
        logger.info(results)
        for record in results:
            for k in list(record):
                if not getattr(Profile, k, None):
                    logger.info(k + ":" + str(record[k]) + " is ignored")
                    del record[k]
            profile = Profile(**record)
            profiles.append(profile)

    return profiles


def query_profile(profile, username=None, project=None):  # noqa: E501
    """query specific profile

    query specific profile # noqa: E501

    :param profile: profile name to query
    :type profile: str
    :param username: creator of the profile
    :type username: str
    :param project: project name
    :type project: str

    :rtype: Profile
    """
    if username is None:
        username = emulab.EMULAB_EXPERIMENT_USER
    if project is None:
        project = emulab.EMULAB_PROJ

    emulab_cmd = '{} sudo python /root/aerpaw/querydb.py {} query_profile {} {}'.format(
        emulab.SSH_BOSS, username, project, profile)
    emulab_stdout = emulab.send_request(emulab_cmd)
    found_profile = None
    if emulab_stdout:
        results = json.loads(emulab_stdout)
        logger.info(results)
        for record in results:
            for k in list(record):
                if not getattr(Profile, k, None):
                    logger.info(k + ":" + str(record[k]) + " is ignored")
                    del record[k]
            found_profile = Profile(**record)
    if found_profile is None:
        abort(404, description="No such profile")
    return found_profile
