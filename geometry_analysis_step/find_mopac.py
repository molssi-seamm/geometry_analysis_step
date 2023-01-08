import seamm_util
from pathlib import Path
import os

mopac_error_identifiers = []


def find_mopac():
    # Try the commandline options / config file
    parser = seamm_util.getParser()
    options = parser.get_options()

    if "mopac-step" in options:
        mopac_options = options["mopac-step"]
        exe = mopac_options["mopac_exe"]
        mopac_path = mopac_options["mopac_path"]
        if mopac_path != "":
            exe = str(Path(mopac_path).expanduser().resolve() / exe)

        try:
            mopac_exe = seamm_util.check_executable(exe)
        except FileNotFoundError:
            pass
        else:
            return mopac_exe

    # Next try common locations
    try:
        mopac_exe = "/opt/mopac/mopac"

        if os.path.isfile(mopac_exe) is False:
            raise FileNotFoundError(
                'The directory "/opt/mopac/" exists, but the executable \
                "mopac" is not there'
            )
    except FileNotFoundError:
        try:
            mopac_path = os.path.split(os.environ["mopac"])[0]
            mopac_exe = mopac_path + "mopac"

            if os.path.isfile(mopac_exe) is False:
                raise FileNotFoundError(
                    'The environment variable "mopac" is defined, but \
                            the executable "mopac" is not there'
                )
        except (KeyError, FileNotFoundError):
            try:
                mopac_exe = Path(os.environ["MOPAC_LICENSE"]) / "mopac"
                mopac_exe = str(mopac_exe)

                if os.path.isfile(mopac_exe) is False:
                    raise FileNotFoundError(
                        'The environment variable "mopac" is defined, but the \
                                executable "mopac" is not there'
                    )

            except (KeyError, FileNotFoundError):
                try:
                    mopac_exe = seamm_util.check_executable("mopac")
                except FileNotFoundError:
                    return None

    return mopac_exe
