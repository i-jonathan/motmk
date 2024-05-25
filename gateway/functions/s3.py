import random
import string


def upload_file_to_s3() -> str:
    """
    unused parameters are file, bucket, object_name
    this would manage uploading file and returning the file path
    since no s3 details, it would just return a random string as the path
    :return: path to s3 object
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
