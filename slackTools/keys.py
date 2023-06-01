import os
import toml


def load(filepath=None, verbose=False):
    '''Load slack keys, searching the following locations:
    - 1st: Provided filepath
    - 2nd: Default local storage location in project root directory under .slack.key.toml
    - 3rd: Default global storage location in home directory under ~/.slack/slack.key.toml
    '''
    filepath_default_local = os.path.expanduser('slack.key.toml')
    filepath_default_local_hidden = os.path.expanduser('.slack.key.toml')
    filepath_default_global = os.path.expanduser('~/.slack/slack.key.toml')

    keypath = None
    if filepath and filepath is not None: # Check provided filepath
        if os.path.isfile(filepath):
            keypath = filepath
        else:
            print(f"<?> Failed to find Slack keys file at {filepath}." \
                " Searching default locations...")

    # Default local
    if not keypath and os.path.isfile(filepath_default_local):
        keypath = filepath_default_local

    # Default local hidden
    if not keypath and os.path.isfile(filepath_default_local_hidden):
        keypath = filepath_default_local_hidden

    # Default global
    elif not keypath and os.path.isfile(filepath_default_global):
        keypath = filepath_default_global

    # Failed
    elif not keypath:
        raise FileNotFoundError(
            "<?> Failed to find Slack key file." \
            "\nPlease provide a valid path to a Slack keys file." \
            "\nConsider placing a Slack Keys in the default file locations:" \
            f"\n1. Local default: {filepath_default_local}" \
            f"\n2. Local default hidden: {filepath_default_local_hidden}" \
            f"\n3. Global default: {filepath_default_global}."
        )

    if verbose:
        print(f"Retrieving Slack Keys from {keypath} ... ", sep='', end='')
    data = toml.load(keypath)
    if verbose:
        print("Done!")
    return data


# TESTING
if __name__ == "__main__":
    load("slack.key.toml", verbose=True)
    load("wrong.key.toml", verbose=True)
