Setup
-----

First install the requests package by running:

    pip install requests

Ensure your ~/.zendesk.cfg is already configured.
You can use your API token information as found at https://support.datastax.com/settings/api.
(You will need ZenDesk admin access to view this page.)
This is mine:

    [ZenDesk]
    email = joaquin@<domain>.com/token
    pass = TOKEN

    [Downloader]
    download_directory = /Users/joaquin/Downloads/support
    run_open = True
    open_program = subl

Then perhaps something simple like:

    sudo ln -s ~/repos/zendesk_downloader/download /usr/local/bin/download

Note: `subl` is an alias that opens Sublime Text 2 and `subl <folder-path>` opens the entire folder in Sublime.
You can choose any command you want, including `open`, which opens a Finder window.

Usage
-----

    download 1828

After that, all attachments are downloaded into the folder

    <download_directory>/<organization-id>/<ticket-id>/<filename>_<attachment-id>.<file-ext>

where:

* `.tar.gz` and `.zip` files are extracted into their proper folders
* file creation and modified dates are set to the original upload date
* files with no extensions are automatically fixed with at .txt (to make it easier for OSX to open files)

Purpose
-------

* Allows filesystems to remain clutterless with support tickets
* Have all organization files ready to easily be grepped
* Ensure that we don't have many `cassandra.yaml (30)` files (maybe just OSX)
* Keep files organized by date of attachment, not download
* Automatically extract compressed information
