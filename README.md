Setup
-----

Ensure your ~/.zendesk.cfg is already configured. This is mine:

    [ZenDesk]
    email = joaquin@datastax.com
    pass = <This can be blank>

    [Downloader]
    download_directory = /Users/joaquin/Downloads/support
    run_open = False

Then perhaps something simple like:

    sudo ln -s ~/repos/support_tool/zendesk_downloader/download /usr/local/bin/download

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
