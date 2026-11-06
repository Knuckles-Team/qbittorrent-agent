"""qBittorrent WebUI API client: one method per upstream operation.

Written by ``scripts/generate_api_client.py`` from
``tests/fixtures/upstream_operations.json`` (qBittorrent release-5.2.4 src/webui/api/*controller.{h,cpp} and src/webui/webapplication.h (POST-only actions)). Every method is served
as one typed MCP tool ``qbittorrent_<scope>_<action>``
(CONN-QBITTORRENT-AGENT-SURFACE-R001).
"""

# ruff: noqa: E501, A002

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from qbittorrent_agent.api.api_client_base import BaseApiClient


class AppApi(BaseApiClient):
    """The `app` scope of the WebUI API."""

    def app_webapi_version(self) -> Any:
        """Get the WebUI API version.

        GET /api/v2/app/webapiVersion
        """
        return self._call("GET", "app/webapiVersion")

    def app_version(self) -> Any:
        """Get the qBittorrent application version.

        GET /api/v2/app/version
        """
        return self._call("GET", "app/version")

    def app_build_info(self) -> Any:
        """Get build info: Qt, libtorrent, Boost, OpenSSL, zlib versions and bitness.

        GET /api/v2/app/buildInfo
        """
        return self._call("GET", "app/buildInfo")

    def app_process_info(self) -> Any:
        """Get process info of the running qBittorrent.

        GET /api/v2/app/processInfo
        """
        return self._call("GET", "app/processInfo")

    def app_shutdown(self) -> Any:
        """Shut down the qBittorrent application.

        POST /api/v2/app/shutdown
        """
        return self._call("POST", "app/shutdown")

    def app_preferences(self) -> Any:
        """Get all application preferences.

        GET /api/v2/app/preferences
        """
        return self._call("GET", "app/preferences")

    def app_set_preferences(
        self,
        *,
        preferences: Annotated[
            dict[str, Any], Field(description="JSON object of the preferences to set")
        ],
    ) -> Any:
        """Set application preferences; only the keys sent change.

        POST /api/v2/app/setPreferences
        """
        return self._call("POST", "app/setPreferences", {"json": preferences})

    def app_default_save_path(self) -> Any:
        """Get the default save path.

        GET /api/v2/app/defaultSavePath
        """
        return self._call("GET", "app/defaultSavePath")

    def app_send_test_email(self) -> Any:
        """Send a test email with the configured email notification settings.

        POST /api/v2/app/sendTestEmail
        """
        return self._call("POST", "app/sendTestEmail")

    def app_get_directory_content(
        self,
        *,
        dir_path: Annotated[
            str, Field(description="Directory on the qBittorrent host")
        ],
        mode: Annotated[
            str | None, Field(description="1 = alternative limits on, 0 = off")
        ] = None,
        with_metadata: Annotated[bool | None, Field(description="withMetadata")] = None,
    ) -> Any:
        """List the content of a directory on the qBittorrent host.

        GET /api/v2/app/getDirectoryContent
        """
        return self._call(
            "GET",
            "app/getDirectoryContent",
            {"dirPath": dir_path, "mode": mode, "withMetadata": with_metadata},
        )

    def app_cookies(self) -> Any:
        """Get the cookies used for downloading torrents and RSS.

        GET /api/v2/app/cookies
        """
        return self._call("GET", "app/cookies")

    def app_set_cookies(
        self,
        *,
        cookies: Annotated[
            list[dict[str, Any]], Field(description="JSON array of cookies")
        ],
    ) -> Any:
        """Set the cookies used for downloading torrents and RSS.

        POST /api/v2/app/setCookies
        """
        return self._call("POST", "app/setCookies", {"cookies": cookies})

    def app_rotate_api_key(self) -> Any:
        """Create or replace the WebUI API key.

        POST /api/v2/app/rotateAPIKey
        """
        return self._call("POST", "app/rotateAPIKey")

    def app_delete_api_key(self) -> Any:
        """Delete the WebUI API key.

        POST /api/v2/app/deleteAPIKey
        """
        return self._call("POST", "app/deleteAPIKey")

    def app_network_interface_list(self) -> Any:
        """List the network interfaces.

        GET /api/v2/app/networkInterfaceList
        """
        return self._call("GET", "app/networkInterfaceList")

    def app_network_interface_address_list(
        self, *, iface: Annotated[str, Field(description="iface")]
    ) -> Any:
        """List the addresses of a network interface.

        GET /api/v2/app/networkInterfaceAddressList
        """
        return self._call("GET", "app/networkInterfaceAddressList", {"iface": iface})


class ClientDataApi(BaseApiClient):
    """The `clientdata` scope of the WebUI API."""

    def clientdata_load(
        self,
        *,
        keys: Annotated[
            list[str] | None, Field(description="JSON array of client-data keys")
        ] = None,
    ) -> Any:
        """Load WebUI client data stored on the server.

        GET /api/v2/clientdata/load
        """
        return self._call("GET", "clientdata/load", {"keys": keys})

    def clientdata_store(
        self,
        *,
        data: Annotated[
            dict[str, Any], Field(description="JSON object of client data to store")
        ],
    ) -> Any:
        """Store WebUI client data on the server.

        POST /api/v2/clientdata/store
        """
        return self._call("POST", "clientdata/store", {"data": data})


class LogApi(BaseApiClient):
    """The `log` scope of the WebUI API."""

    def log_main(
        self,
        *,
        normal: Annotated[bool | None, Field(description="normal")] = None,
        info: Annotated[bool | None, Field(description="info")] = None,
        warning: Annotated[bool | None, Field(description="warning")] = None,
        critical: Annotated[bool | None, Field(description="critical")] = None,
        last_known_id: Annotated[
            int | None, Field(description="Only entries newer than this id")
        ] = None,
    ) -> Any:
        """Get the main log, filtered by severity.

        GET /api/v2/log/main
        """
        return self._call(
            "GET",
            "log/main",
            {
                "normal": normal,
                "info": info,
                "warning": warning,
                "critical": critical,
                "last_known_id": last_known_id,
            },
        )

    def log_peers(
        self,
        *,
        last_known_id: Annotated[
            int | None, Field(description="Only entries newer than this id")
        ] = None,
    ) -> Any:
        """Get the peer log.

        GET /api/v2/log/peers
        """
        return self._call("GET", "log/peers", {"last_known_id": last_known_id})


class RssApi(BaseApiClient):
    """The `rss` scope of the WebUI API."""

    def rss_add_folder(
        self,
        *,
        path: Annotated[
            str, Field(description="RSS item path, folders separated by `\\\\`")
        ],
    ) -> Any:
        """Add an RSS folder.

        POST /api/v2/rss/addFolder
        """
        return self._call("POST", "rss/addFolder", {"path": path})

    def rss_add_feed(
        self,
        *,
        url: Annotated[str, Field(description="url")],
        path: Annotated[
            str, Field(description="RSS item path, folders separated by `\\\\`")
        ],
        refresh_interval: Annotated[
            int | None, Field(description="refreshInterval")
        ] = None,
    ) -> Any:
        """Add an RSS feed.

        POST /api/v2/rss/addFeed
        """
        return self._call(
            "POST",
            "rss/addFeed",
            {"url": url, "path": path, "refreshInterval": refresh_interval},
        )

    def rss_set_feed_url(
        self,
        *,
        path: Annotated[
            str, Field(description="RSS item path, folders separated by `\\\\`")
        ],
        url: Annotated[str, Field(description="url")],
    ) -> Any:
        """Change the URL of an RSS feed.

        POST /api/v2/rss/setFeedURL
        """
        return self._call("POST", "rss/setFeedURL", {"path": path, "url": url})

    def rss_set_feed_refresh_interval(
        self,
        *,
        refresh_interval: Annotated[int, Field(description="refreshInterval")],
        path: Annotated[
            str, Field(description="RSS item path, folders separated by `\\\\`")
        ],
    ) -> Any:
        """Set the refresh interval of an RSS feed.

        GET /api/v2/rss/setFeedRefreshInterval
        """
        return self._call(
            "GET",
            "rss/setFeedRefreshInterval",
            {"refreshInterval": refresh_interval, "path": path},
        )

    def rss_remove_item(
        self,
        *,
        path: Annotated[
            str, Field(description="RSS item path, folders separated by `\\\\`")
        ],
    ) -> Any:
        """Remove an RSS feed or folder.

        POST /api/v2/rss/removeItem
        """
        return self._call("POST", "rss/removeItem", {"path": path})

    def rss_move_item(
        self,
        *,
        item_path: Annotated[str, Field(description="RSS item path")],
        dest_path: Annotated[str, Field(description="Destination RSS path")],
    ) -> Any:
        """Move or rename an RSS feed or folder.

        POST /api/v2/rss/moveItem
        """
        return self._call(
            "POST", "rss/moveItem", {"itemPath": item_path, "destPath": dest_path}
        )

    def rss_items(
        self, *, with_data: Annotated[bool | None, Field(description="withData")] = None
    ) -> Any:
        """List RSS feeds and folders, optionally with articles.

        GET /api/v2/rss/items
        """
        return self._call("GET", "rss/items", {"withData": with_data})

    def rss_mark_as_read(
        self,
        *,
        item_path: Annotated[str, Field(description="RSS item path")],
        article_id: Annotated[str | None, Field(description="articleId")] = None,
    ) -> Any:
        """Mark an RSS item or article as read.

        POST /api/v2/rss/markAsRead
        """
        return self._call(
            "POST", "rss/markAsRead", {"itemPath": item_path, "articleId": article_id}
        )

    def rss_refresh_item(
        self, *, item_path: Annotated[str, Field(description="RSS item path")]
    ) -> Any:
        """Refresh an RSS feed or folder.

        POST /api/v2/rss/refreshItem
        """
        return self._call("POST", "rss/refreshItem", {"itemPath": item_path})

    def rss_set_rule(
        self,
        *,
        rule_name: Annotated[str, Field(description="RSS rule name")],
        rule_def: Annotated[dict[str, Any], Field(description="JSON rule definition")],
    ) -> Any:
        """Create or update an RSS auto-download rule.

        POST /api/v2/rss/setRule
        """
        return self._call(
            "POST", "rss/setRule", {"ruleName": rule_name, "ruleDef": rule_def}
        )

    def rss_rename_rule(
        self,
        *,
        rule_name: Annotated[str, Field(description="RSS rule name")],
        new_rule_name: Annotated[str, Field(description="newRuleName")],
    ) -> Any:
        """Rename an RSS auto-download rule.

        POST /api/v2/rss/renameRule
        """
        return self._call(
            "POST",
            "rss/renameRule",
            {"ruleName": rule_name, "newRuleName": new_rule_name},
        )

    def rss_remove_rule(
        self, *, rule_name: Annotated[str, Field(description="RSS rule name")]
    ) -> Any:
        """Remove an RSS auto-download rule.

        POST /api/v2/rss/removeRule
        """
        return self._call("POST", "rss/removeRule", {"ruleName": rule_name})

    def rss_rules(self) -> Any:
        """List RSS auto-download rules.

        GET /api/v2/rss/rules
        """
        return self._call("GET", "rss/rules")

    def rss_matching_articles(
        self, *, rule_name: Annotated[str, Field(description="RSS rule name")]
    ) -> Any:
        """List the articles that match an RSS auto-download rule.

        GET /api/v2/rss/matchingArticles
        """
        return self._call("GET", "rss/matchingArticles", {"ruleName": rule_name})


class SearchApi(BaseApiClient):
    """The `search` scope of the WebUI API."""

    def search_start(
        self,
        *,
        pattern: Annotated[str, Field(description="Search text")],
        category: Annotated[str, Field(description="Category name")],
        plugins: Annotated[
            str,
            Field(
                description="Plugins to use: names separated by `|`, `all` or `enabled`"
            ),
        ],
    ) -> Any:
        """Start a search job with the search plugins.

        POST /api/v2/search/start
        """
        return self._call(
            "POST",
            "search/start",
            {"pattern": pattern, "category": category, "plugins": plugins},
        )

    def search_stop(
        self,
        *,
        id: Annotated[
            int,
            Field(
                description="Id (search job id; for torrents/setSavePath and setDownloadPath: hashes separated by `|`)"
            ),
        ],
    ) -> Any:
        """Stop a search job.

        POST /api/v2/search/stop
        """
        return self._call("POST", "search/stop", {"id": id})

    def search_status(
        self,
        *,
        id: Annotated[
            int | None,
            Field(
                description="Id (search job id; for torrents/setSavePath and setDownloadPath: hashes separated by `|`)"
            ),
        ] = None,
    ) -> Any:
        """Get the status of one or all search jobs.

        GET /api/v2/search/status
        """
        return self._call("GET", "search/status", {"id": id})

    def search_results(
        self,
        *,
        id: Annotated[
            int,
            Field(
                description="Id (search job id; for torrents/setSavePath and setDownloadPath: hashes separated by `|`)"
            ),
        ],
        limit: Annotated[
            int | None, Field(description="At most this many results")
        ] = None,
        offset: Annotated[
            int | None, Field(description="Skip this many results")
        ] = None,
    ) -> Any:
        """Get the results of a search job.

        GET /api/v2/search/results
        """
        return self._call(
            "GET", "search/results", {"id": id, "limit": limit, "offset": offset}
        )

    def search_delete(
        self,
        *,
        id: Annotated[
            int,
            Field(
                description="Id (search job id; for torrents/setSavePath and setDownloadPath: hashes separated by `|`)"
            ),
        ],
    ) -> Any:
        """Delete a search job.

        POST /api/v2/search/delete
        """
        return self._call("POST", "search/delete", {"id": id})

    def search_download_torrent(
        self,
        *,
        torrent_url: Annotated[str, Field(description="torrentUrl")],
        plugin_name: Annotated[str, Field(description="pluginName")],
    ) -> Any:
        """Download a torrent found by a search plugin.

        GET /api/v2/search/downloadTorrent
        """
        return self._call(
            "GET",
            "search/downloadTorrent",
            {"torrentUrl": torrent_url, "pluginName": plugin_name},
        )

    def search_plugins(self) -> Any:
        """List the search plugins.

        GET /api/v2/search/plugins
        """
        return self._call("GET", "search/plugins")

    def search_install_plugin(
        self,
        *,
        sources: Annotated[
            str, Field(description="Plugin URLs or paths separated by `|`")
        ],
    ) -> Any:
        """Install search plugins from URLs or paths.

        POST /api/v2/search/installPlugin
        """
        return self._call("POST", "search/installPlugin", {"sources": sources})

    def search_uninstall_plugin(
        self,
        *,
        names: Annotated[str, Field(description="Plugin names separated by `|`")],
    ) -> Any:
        """Uninstall search plugins.

        POST /api/v2/search/uninstallPlugin
        """
        return self._call("POST", "search/uninstallPlugin", {"names": names})

    def search_enable_plugin(
        self,
        *,
        names: Annotated[str, Field(description="Plugin names separated by `|`")],
        enable: Annotated[bool, Field(description="true to enable, false to disable")],
    ) -> Any:
        """Enable or disable search plugins.

        POST /api/v2/search/enablePlugin
        """
        return self._call(
            "POST", "search/enablePlugin", {"names": names, "enable": enable}
        )

    def search_update_plugins(self) -> Any:
        """Update all search plugins.

        POST /api/v2/search/updatePlugins
        """
        return self._call("POST", "search/updatePlugins")


class SyncApi(BaseApiClient):
    """The `sync` scope of the WebUI API."""

    def sync_maindata(
        self,
        *,
        rid: Annotated[
            int | None,
            Field(description="Response id from the last sync call (0 = full state)"),
        ] = None,
    ) -> Any:
        """Get the main data changes since a response id (full state when rid is 0).

        GET /api/v2/sync/maindata
        """
        return self._call("GET", "sync/maindata", {"rid": rid})

    def sync_torrent_peers(
        self,
        *,
        hash: Annotated[str | None, Field(description="Torrent hash")] = None,
        rid: Annotated[
            int | None,
            Field(description="Response id from the last sync call (0 = full state)"),
        ] = None,
    ) -> Any:
        """Get the peer data changes of one torrent since a response id.

        GET /api/v2/sync/torrentPeers
        """
        return self._call("GET", "sync/torrentPeers", {"hash": hash, "rid": rid})


class TorrentCreatorApi(BaseApiClient):
    """The `torrentcreator` scope of the WebUI API."""

    def torrentcreator_add_task(
        self,
        *,
        source_path: Annotated[
            str, Field(description="File or folder on the qBittorrent host")
        ],
        private: Annotated[bool | None, Field(description="private")] = None,
        format: Annotated[str | None, Field(description="format")] = None,
        optimize_alignment: Annotated[
            bool | None, Field(description="optimizeAlignment")
        ] = None,
        padded_file_size_limit: Annotated[
            int | None, Field(description="paddedFileSizeLimit")
        ] = None,
        piece_size: Annotated[int | None, Field(description="pieceSize")] = None,
        torrent_file_path: Annotated[
            str | None, Field(description="torrentFilePath")
        ] = None,
        comment: Annotated[str | None, Field(description="comment")] = None,
        source: Annotated[
            str | None, Field(description="Magnet link, URL or info-hash")
        ] = None,
        trackers: Annotated[str | None, Field(description="trackers")] = None,
        url_seeds: Annotated[str | None, Field(description="urlSeeds")] = None,
        start_seeding: Annotated[bool | None, Field(description="startSeeding")] = None,
    ) -> Any:
        """Create a torrent from a file or folder on the qBittorrent host.

        POST /api/v2/torrentcreator/addTask
        """
        return self._call(
            "POST",
            "torrentcreator/addTask",
            {
                "sourcePath": source_path,
                "private": private,
                "format": format,
                "optimizeAlignment": optimize_alignment,
                "paddedFileSizeLimit": padded_file_size_limit,
                "pieceSize": piece_size,
                "torrentFilePath": torrent_file_path,
                "comment": comment,
                "source": source,
                "trackers": trackers,
                "urlSeeds": url_seeds,
                "startSeeding": start_seeding,
            },
        )

    def torrentcreator_status(
        self,
        *,
        task_i_d: Annotated[
            str | None, Field(description="Torrent-creator task id")
        ] = None,
    ) -> Any:
        """Get the status of one or all torrent-creator tasks.

        GET /api/v2/torrentcreator/status
        """
        return self._call("GET", "torrentcreator/status", {"taskID": task_i_d})

    def torrentcreator_torrent_file(
        self, *, task_i_d: Annotated[str, Field(description="Torrent-creator task id")]
    ) -> Any:
        """Get the .torrent file a creator task produced.

        GET /api/v2/torrentcreator/torrentFile
        """
        return self._call("GET", "torrentcreator/torrentFile", {"taskID": task_i_d})

    def torrentcreator_delete_task(
        self, *, task_i_d: Annotated[str, Field(description="Torrent-creator task id")]
    ) -> Any:
        """Delete a torrent-creator task.

        POST /api/v2/torrentcreator/deleteTask
        """
        return self._call("POST", "torrentcreator/deleteTask", {"taskID": task_i_d})


class TorrentsApi(BaseApiClient):
    """The `torrents` scope of the WebUI API."""

    def torrents_count(self) -> Any:
        """Count the torrents.

        GET /api/v2/torrents/count
        """
        return self._call("GET", "torrents/count")

    def torrents_info(
        self,
        *,
        filter: Annotated[
            str | None,
            Field(
                description="State filter: all, downloading, seeding, completed, stopped, running, active, inactive, stalled, errored, ..."
            ),
        ] = None,
        category: Annotated[str | None, Field(description="Category name")] = None,
        tag: Annotated[str | None, Field(description="Tag name")] = None,
        sort: Annotated[
            str | None,
            Field(
                description="Field to sort by (any torrent property, for example added_on)"
            ),
        ] = None,
        reverse: Annotated[
            bool | None, Field(description="Reverse the sort order")
        ] = None,
        limit: Annotated[
            int | None, Field(description="At most this many torrents")
        ] = None,
        offset: Annotated[
            int | None,
            Field(description="Skip this many torrents (negative counts from the end)"),
        ] = None,
        hashes: Annotated[
            str | None, Field(description="Torrent hashes separated by `|`, or `all`")
        ] = None,
        private: Annotated[
            bool | None,
            Field(description="Only private (true) or public (false) torrents"),
        ] = None,
        include_files: Annotated[
            bool | None, Field(description="Include each torrent's files")
        ] = None,
        include_trackers: Annotated[
            bool | None, Field(description="Include each torrent's trackers")
        ] = None,
    ) -> Any:
        """List torrents, filtered and sorted.

        GET /api/v2/torrents/info
        """
        return self._call(
            "GET",
            "torrents/info",
            {
                "filter": filter,
                "category": category,
                "tag": tag,
                "sort": sort,
                "reverse": reverse,
                "limit": limit,
                "offset": offset,
                "hashes": hashes,
                "private": private,
                "includeFiles": include_files,
                "includeTrackers": include_trackers,
            },
        )

    def torrents_properties(
        self, *, hash: Annotated[str, Field(description="Torrent hash")]
    ) -> Any:
        """Get the generic properties of one torrent.

        GET /api/v2/torrents/properties
        """
        return self._call("GET", "torrents/properties", {"hash": hash})

    def torrents_trackers(
        self, *, hash: Annotated[str, Field(description="Torrent hash")]
    ) -> Any:
        """List the trackers of one torrent.

        GET /api/v2/torrents/trackers
        """
        return self._call("GET", "torrents/trackers", {"hash": hash})

    def torrents_webseeds(
        self, *, hash: Annotated[str, Field(description="Torrent hash")]
    ) -> Any:
        """List the web seeds of one torrent.

        GET /api/v2/torrents/webseeds
        """
        return self._call("GET", "torrents/webseeds", {"hash": hash})

    def torrents_add_web_seeds(
        self,
        *,
        urls: Annotated[
            str,
            Field(
                description="URLs; separate several with `|` (torrents/add: newline)"
            ),
        ],
        hash: Annotated[str, Field(description="Torrent hash")],
    ) -> Any:
        """Add web seeds to a torrent.

        POST /api/v2/torrents/addWebSeeds
        """
        return self._call("POST", "torrents/addWebSeeds", {"urls": urls, "hash": hash})

    def torrents_edit_web_seed(
        self,
        *,
        hash: Annotated[str, Field(description="Torrent hash")],
        orig_url: Annotated[str, Field(description="origUrl")],
        new_url: Annotated[str, Field(description="newUrl")],
    ) -> Any:
        """Replace a web seed URL of a torrent.

        POST /api/v2/torrents/editWebSeed
        """
        return self._call(
            "POST",
            "torrents/editWebSeed",
            {"hash": hash, "origUrl": orig_url, "newUrl": new_url},
        )

    def torrents_remove_web_seeds(
        self,
        *,
        urls: Annotated[
            str,
            Field(
                description="URLs; separate several with `|` (torrents/add: newline)"
            ),
        ],
        hash: Annotated[str, Field(description="Torrent hash")],
    ) -> Any:
        """Remove web seeds from a torrent.

        POST /api/v2/torrents/removeWebSeeds
        """
        return self._call(
            "POST", "torrents/removeWebSeeds", {"urls": urls, "hash": hash}
        )

    def torrents_files(
        self, *, hash: Annotated[str, Field(description="Torrent hash")]
    ) -> Any:
        """List the files of one torrent.

        GET /api/v2/torrents/files
        """
        return self._call("GET", "torrents/files", {"hash": hash})

    def torrents_piece_hashes(
        self, *, hash: Annotated[str, Field(description="Torrent hash")]
    ) -> Any:
        """Get the piece hashes of one torrent.

        GET /api/v2/torrents/pieceHashes
        """
        return self._call("GET", "torrents/pieceHashes", {"hash": hash})

    def torrents_piece_states(
        self, *, hash: Annotated[str, Field(description="Torrent hash")]
    ) -> Any:
        """Get the piece states of one torrent.

        GET /api/v2/torrents/pieceStates
        """
        return self._call("GET", "torrents/pieceStates", {"hash": hash})

    def torrents_piece_availability(
        self, *, hash: Annotated[str, Field(description="Torrent hash")]
    ) -> Any:
        """Get the piece availability of one torrent.

        GET /api/v2/torrents/pieceAvailability
        """
        return self._call("GET", "torrents/pieceAvailability", {"hash": hash})

    def torrents_start(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Start (resume) torrents.

        POST /api/v2/torrents/start
        """
        return self._call("POST", "torrents/start", {"hashes": hashes})

    def torrents_stop(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Stop (pause) torrents.

        POST /api/v2/torrents/stop
        """
        return self._call("POST", "torrents/stop", {"hashes": hashes})

    def torrents_recheck(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Recheck torrents.

        POST /api/v2/torrents/recheck
        """
        return self._call("POST", "torrents/recheck", {"hashes": hashes})

    def torrents_reannounce(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        urls: Annotated[
            str | None,
            Field(
                description="URLs; separate several with `|` (torrents/add: newline)"
            ),
        ] = None,
    ) -> Any:
        """Reannounce torrents to their trackers.

        POST /api/v2/torrents/reannounce
        """
        return self._call(
            "POST", "torrents/reannounce", {"hashes": hashes, "urls": urls}
        )

    def torrents_rename(
        self,
        *,
        hash: Annotated[str, Field(description="Torrent hash")],
        name: Annotated[str, Field(description="name")],
    ) -> Any:
        """Rename a torrent.

        POST /api/v2/torrents/rename
        """
        return self._call("POST", "torrents/rename", {"hash": hash, "name": name})

    def torrents_set_comment(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        comment: Annotated[str, Field(description="comment")],
    ) -> Any:
        """Set the comment of torrents.

        POST /api/v2/torrents/setComment
        """
        return self._call(
            "POST", "torrents/setComment", {"hashes": hashes, "comment": comment}
        )

    def torrents_set_category(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        category: Annotated[str, Field(description="Category name")],
    ) -> Any:
        """Set the category of torrents.

        POST /api/v2/torrents/setCategory
        """
        return self._call(
            "POST", "torrents/setCategory", {"hashes": hashes, "category": category}
        )

    def torrents_create_category(
        self,
        *,
        category: Annotated[str, Field(description="Category name")],
        save_path: Annotated[str | None, Field(description="Save path")] = None,
        download_path_enabled: Annotated[
            bool | None, Field(description="downloadPathEnabled")
        ] = None,
        download_path: Annotated[
            str | None, Field(description="Incomplete-download path")
        ] = None,
    ) -> Any:
        """Create a category.

        POST /api/v2/torrents/createCategory
        """
        return self._call(
            "POST",
            "torrents/createCategory",
            {
                "category": category,
                "savePath": save_path,
                "downloadPathEnabled": download_path_enabled,
                "downloadPath": download_path,
            },
        )

    def torrents_edit_category(
        self,
        *,
        category: Annotated[str, Field(description="Category name")],
        save_path: Annotated[str, Field(description="Save path")],
        download_path_enabled: Annotated[
            bool | None, Field(description="downloadPathEnabled")
        ] = None,
        download_path: Annotated[
            str | None, Field(description="Incomplete-download path")
        ] = None,
    ) -> Any:
        """Edit a category's save and download paths.

        POST /api/v2/torrents/editCategory
        """
        return self._call(
            "POST",
            "torrents/editCategory",
            {
                "category": category,
                "savePath": save_path,
                "downloadPathEnabled": download_path_enabled,
                "downloadPath": download_path,
            },
        )

    def torrents_remove_categories(
        self,
        *,
        categories: Annotated[
            str, Field(description="Category names separated by newline")
        ],
    ) -> Any:
        """Remove categories.

        POST /api/v2/torrents/removeCategories
        """
        return self._call(
            "POST", "torrents/removeCategories", {"categories": categories}
        )

    def torrents_categories(self) -> Any:
        """List all categories.

        GET /api/v2/torrents/categories
        """
        return self._call("GET", "torrents/categories")

    def torrents_add_tags(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        tags: Annotated[str, Field(description="Comma-separated tag names")],
    ) -> Any:
        """Add tags to torrents.

        POST /api/v2/torrents/addTags
        """
        return self._call("POST", "torrents/addTags", {"hashes": hashes, "tags": tags})

    def torrents_set_tags(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        tags: Annotated[str, Field(description="Comma-separated tag names")],
    ) -> Any:
        """Replace the tags of torrents.

        POST /api/v2/torrents/setTags
        """
        return self._call("POST", "torrents/setTags", {"hashes": hashes, "tags": tags})

    def torrents_remove_tags(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        tags: Annotated[
            str | None, Field(description="Comma-separated tag names")
        ] = None,
    ) -> Any:
        """Remove tags from torrents (all tags when none are given).

        POST /api/v2/torrents/removeTags
        """
        return self._call(
            "POST", "torrents/removeTags", {"hashes": hashes, "tags": tags}
        )

    def torrents_create_tags(
        self, *, tags: Annotated[str, Field(description="Comma-separated tag names")]
    ) -> Any:
        """Create tags.

        POST /api/v2/torrents/createTags
        """
        return self._call("POST", "torrents/createTags", {"tags": tags})

    def torrents_delete_tags(
        self, *, tags: Annotated[str, Field(description="Comma-separated tag names")]
    ) -> Any:
        """Delete tags.

        POST /api/v2/torrents/deleteTags
        """
        return self._call("POST", "torrents/deleteTags", {"tags": tags})

    def torrents_tags(self) -> Any:
        """List all tags.

        GET /api/v2/torrents/tags
        """
        return self._call("GET", "torrents/tags")

    def torrents_add(
        self,
        *,
        urls: Annotated[
            str | None,
            Field(
                description="URLs; separate several with `|` (torrents/add: newline)"
            ),
        ] = None,
        skip_checking: Annotated[
            bool | None, Field(description="skip_checking")
        ] = None,
        sequential_download: Annotated[
            bool | None, Field(description="sequentialDownload")
        ] = None,
        first_last_piece_prio: Annotated[
            bool | None, Field(description="firstLastPiecePrio")
        ] = None,
        forced: Annotated[bool | None, Field(description="forced")] = None,
        add_to_top_of_queue: Annotated[
            bool | None, Field(description="addToTopOfQueue")
        ] = None,
        stopped: Annotated[bool | None, Field(description="stopped")] = None,
        savepath: Annotated[str | None, Field(description="savepath")] = None,
        download_path: Annotated[
            str | None, Field(description="Incomplete-download path")
        ] = None,
        use_download_path: Annotated[
            bool | None, Field(description="useDownloadPath")
        ] = None,
        category: Annotated[str | None, Field(description="Category name")] = None,
        tags: Annotated[
            str | None, Field(description="Comma-separated tag names")
        ] = None,
        rename: Annotated[str | None, Field(description="rename")] = None,
        up_limit: Annotated[int | None, Field(description="upLimit")] = None,
        dl_limit: Annotated[int | None, Field(description="dlLimit")] = None,
        ratio_limit: Annotated[float | None, Field(description="ratioLimit")] = None,
        seeding_time_limit: Annotated[
            int | None, Field(description="seedingTimeLimit")
        ] = None,
        inactive_seeding_time_limit: Annotated[
            int | None, Field(description="inactiveSeedingTimeLimit")
        ] = None,
        share_limit_action: Annotated[
            str | None, Field(description="shareLimitAction")
        ] = None,
        auto_t_m_m: Annotated[bool | None, Field(description="autoTMM")] = None,
        stop_condition: Annotated[
            str | None, Field(description="stopCondition")
        ] = None,
        content_layout: Annotated[
            str | None, Field(description="contentLayout")
        ] = None,
        file_priorities: Annotated[
            str | None, Field(description="filePriorities")
        ] = None,
        downloader: Annotated[str | None, Field(description="downloader")] = None,
        ssl_certificate: Annotated[
            str | None, Field(description="ssl_certificate")
        ] = None,
        ssl_private_key: Annotated[
            str | None, Field(description="ssl_private_key")
        ] = None,
        ssl_dh_params: Annotated[str | None, Field(description="ssl_dh_params")] = None,
        torrent_files: Annotated[
            dict[str, str] | None,
            Field(description="Uploaded .torrent files: file name to base64 content"),
        ] = None,
    ) -> Any:
        """Add torrents from URLs, magnet links or uploaded .torrent files.

        POST /api/v2/torrents/add
        """
        return self._call(
            "POST",
            "torrents/add",
            {
                "urls": urls,
                "skip_checking": skip_checking,
                "sequentialDownload": sequential_download,
                "firstLastPiecePrio": first_last_piece_prio,
                "forced": forced,
                "addToTopOfQueue": add_to_top_of_queue,
                "stopped": stopped,
                "savepath": savepath,
                "downloadPath": download_path,
                "useDownloadPath": use_download_path,
                "category": category,
                "tags": tags,
                "rename": rename,
                "upLimit": up_limit,
                "dlLimit": dl_limit,
                "ratioLimit": ratio_limit,
                "seedingTimeLimit": seeding_time_limit,
                "inactiveSeedingTimeLimit": inactive_seeding_time_limit,
                "shareLimitAction": share_limit_action,
                "autoTMM": auto_t_m_m,
                "stopCondition": stop_condition,
                "contentLayout": content_layout,
                "filePriorities": file_priorities,
                "downloader": downloader,
                "ssl_certificate": ssl_certificate,
                "ssl_private_key": ssl_private_key,
                "ssl_dh_params": ssl_dh_params,
            },
            torrent_files,
        )

    def torrents_delete(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        delete_files: Annotated[
            bool, Field(description="Also delete the downloaded files")
        ],
    ) -> Any:
        """Delete torrents, optionally with their downloaded files.

        POST /api/v2/torrents/delete
        """
        return self._call(
            "POST", "torrents/delete", {"hashes": hashes, "deleteFiles": delete_files}
        )

    def torrents_add_trackers(
        self,
        *,
        urls: Annotated[
            str,
            Field(
                description="URLs; separate several with `|` (torrents/add: newline)"
            ),
        ],
        hash: Annotated[str, Field(description="Torrent hash")],
    ) -> Any:
        """Add trackers to a torrent.

        POST /api/v2/torrents/addTrackers
        """
        return self._call("POST", "torrents/addTrackers", {"urls": urls, "hash": hash})

    def torrents_edit_tracker(
        self,
        *,
        hash: Annotated[str, Field(description="Torrent hash")],
        url: Annotated[str, Field(description="url")],
        new_url: Annotated[str | None, Field(description="newUrl")] = None,
        tier: Annotated[str | None, Field(description="tier")] = None,
    ) -> Any:
        """Replace a tracker URL of a torrent.

        POST /api/v2/torrents/editTracker
        """
        return self._call(
            "POST",
            "torrents/editTracker",
            {"hash": hash, "url": url, "newUrl": new_url, "tier": tier},
        )

    def torrents_remove_trackers(
        self,
        *,
        hash: Annotated[str, Field(description="Torrent hash")],
        urls: Annotated[
            str,
            Field(
                description="URLs; separate several with `|` (torrents/add: newline)"
            ),
        ],
    ) -> Any:
        """Remove trackers from a torrent.

        POST /api/v2/torrents/removeTrackers
        """
        return self._call(
            "POST", "torrents/removeTrackers", {"hash": hash, "urls": urls}
        )

    def torrents_add_peers(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        peers: Annotated[str, Field(description="Peers as host:port separated by `|`")],
    ) -> Any:
        """Add peers to torrents.

        POST /api/v2/torrents/addPeers
        """
        return self._call(
            "POST", "torrents/addPeers", {"hashes": hashes, "peers": peers}
        )

    def torrents_file_prio(
        self,
        *,
        hash: Annotated[str, Field(description="Torrent hash")],
        id: Annotated[
            str,
            Field(
                description="Id (search job id; for torrents/setSavePath and setDownloadPath: hashes separated by `|`)"
            ),
        ],
        priority: Annotated[
            int, Field(description="File priority: 0 skip, 1 normal, 6 high, 7 maximal")
        ],
    ) -> Any:
        """Set the priority of files in a torrent.

        POST /api/v2/torrents/filePrio
        """
        return self._call(
            "POST", "torrents/filePrio", {"hash": hash, "id": id, "priority": priority}
        )

    def torrents_upload_limit(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Get the upload limit of torrents.

        GET /api/v2/torrents/uploadLimit
        """
        return self._call("GET", "torrents/uploadLimit", {"hashes": hashes})

    def torrents_download_limit(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Get the download limit of torrents.

        GET /api/v2/torrents/downloadLimit
        """
        return self._call("GET", "torrents/downloadLimit", {"hashes": hashes})

    def torrents_set_upload_limit(
        self,
        *,
        limit: Annotated[
            int, Field(description="Limit in bytes per second (0 or -1 = unlimited)")
        ],
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Set the upload limit of torrents.

        POST /api/v2/torrents/setUploadLimit
        """
        return self._call(
            "POST", "torrents/setUploadLimit", {"limit": limit, "hashes": hashes}
        )

    def torrents_set_download_limit(
        self,
        *,
        limit: Annotated[
            int, Field(description="Limit in bytes per second (0 or -1 = unlimited)")
        ],
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Set the download limit of torrents.

        POST /api/v2/torrents/setDownloadLimit
        """
        return self._call(
            "POST", "torrents/setDownloadLimit", {"limit": limit, "hashes": hashes}
        )

    def torrents_set_share_limits(
        self,
        *,
        ratio_limit: Annotated[float, Field(description="ratioLimit")],
        seeding_time_limit: Annotated[int, Field(description="seedingTimeLimit")],
        inactive_seeding_time_limit: Annotated[
            int, Field(description="inactiveSeedingTimeLimit")
        ],
        share_limit_action: Annotated[str, Field(description="shareLimitAction")],
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Set the share (ratio and seeding time) limits of torrents.

        POST /api/v2/torrents/setShareLimits
        """
        return self._call(
            "POST",
            "torrents/setShareLimits",
            {
                "ratioLimit": ratio_limit,
                "seedingTimeLimit": seeding_time_limit,
                "inactiveSeedingTimeLimit": inactive_seeding_time_limit,
                "shareLimitAction": share_limit_action,
                "hashes": hashes,
            },
        )

    def torrents_increase_prio(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Raise the queue priority of torrents.

        POST /api/v2/torrents/increasePrio
        """
        return self._call("POST", "torrents/increasePrio", {"hashes": hashes})

    def torrents_decrease_prio(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Lower the queue priority of torrents.

        POST /api/v2/torrents/decreasePrio
        """
        return self._call("POST", "torrents/decreasePrio", {"hashes": hashes})

    def torrents_top_prio(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Move torrents to the top of the queue.

        POST /api/v2/torrents/topPrio
        """
        return self._call("POST", "torrents/topPrio", {"hashes": hashes})

    def torrents_bottom_prio(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Move torrents to the bottom of the queue.

        POST /api/v2/torrents/bottomPrio
        """
        return self._call("POST", "torrents/bottomPrio", {"hashes": hashes})

    def torrents_set_location(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        location: Annotated[str, Field(description="New location of the data")],
    ) -> Any:
        """Move the data of torrents to a new location.

        POST /api/v2/torrents/setLocation
        """
        return self._call(
            "POST", "torrents/setLocation", {"hashes": hashes, "location": location}
        )

    def torrents_set_save_path(
        self,
        *,
        id: Annotated[
            str,
            Field(
                description="Id (search job id; for torrents/setSavePath and setDownloadPath: hashes separated by `|`)"
            ),
        ],
        path: Annotated[
            str, Field(description="RSS item path, folders separated by `\\\\`")
        ],
    ) -> Any:
        """Set the save path of torrents.

        POST /api/v2/torrents/setSavePath
        """
        return self._call("POST", "torrents/setSavePath", {"id": id, "path": path})

    def torrents_set_download_path(
        self,
        *,
        id: Annotated[
            str,
            Field(
                description="Id (search job id; for torrents/setSavePath and setDownloadPath: hashes separated by `|`)"
            ),
        ],
        path: Annotated[
            str, Field(description="RSS item path, folders separated by `\\\\`")
        ],
    ) -> Any:
        """Set the incomplete-download path of torrents.

        POST /api/v2/torrents/setDownloadPath
        """
        return self._call("POST", "torrents/setDownloadPath", {"id": id, "path": path})

    def torrents_set_auto_management(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
        enable: Annotated[bool, Field(description="true to enable, false to disable")],
    ) -> Any:
        """Turn automatic torrent management on or off.

        POST /api/v2/torrents/setAutoManagement
        """
        return self._call(
            "POST", "torrents/setAutoManagement", {"hashes": hashes, "enable": enable}
        )

    def torrents_set_super_seeding(
        self,
        *,
        value: Annotated[bool, Field(description="true to turn on, false to turn off")],
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Turn super seeding on or off.

        POST /api/v2/torrents/setSuperSeeding
        """
        return self._call(
            "POST", "torrents/setSuperSeeding", {"value": value, "hashes": hashes}
        )

    def torrents_set_force_start(
        self,
        *,
        value: Annotated[bool, Field(description="true to turn on, false to turn off")],
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Turn force start on or off.

        POST /api/v2/torrents/setForceStart
        """
        return self._call(
            "POST", "torrents/setForceStart", {"value": value, "hashes": hashes}
        )

    def torrents_toggle_sequential_download(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Toggle sequential download.

        POST /api/v2/torrents/toggleSequentialDownload
        """
        return self._call(
            "POST", "torrents/toggleSequentialDownload", {"hashes": hashes}
        )

    def torrents_toggle_first_last_piece_prio(
        self,
        *,
        hashes: Annotated[
            str, Field(description="Torrent hashes separated by `|`, or `all`")
        ],
    ) -> Any:
        """Toggle first and last piece priority.

        POST /api/v2/torrents/toggleFirstLastPiecePrio
        """
        return self._call(
            "POST", "torrents/toggleFirstLastPiecePrio", {"hashes": hashes}
        )

    def torrents_rename_file(
        self,
        *,
        new_path: Annotated[str, Field(description="New path")],
        hash: Annotated[str, Field(description="Torrent hash")],
        old_path: Annotated[str, Field(description="Current path")],
    ) -> Any:
        """Rename a file in a torrent.

        POST /api/v2/torrents/renameFile
        """
        return self._call(
            "POST",
            "torrents/renameFile",
            {"newPath": new_path, "hash": hash, "oldPath": old_path},
        )

    def torrents_rename_folder(
        self,
        *,
        new_path: Annotated[str, Field(description="New path")],
        hash: Annotated[str, Field(description="Torrent hash")],
        old_path: Annotated[str, Field(description="Current path")],
    ) -> Any:
        """Rename a folder in a torrent.

        POST /api/v2/torrents/renameFolder
        """
        return self._call(
            "POST",
            "torrents/renameFolder",
            {"newPath": new_path, "hash": hash, "oldPath": old_path},
        )

    def torrents_export(
        self, *, hash: Annotated[str, Field(description="Torrent hash")]
    ) -> Any:
        """Export a torrent as a .torrent file.

        GET /api/v2/torrents/export
        """
        return self._call("GET", "torrents/export", {"hash": hash})

    def torrents_ssl_parameters(
        self, *, hash: Annotated[str, Field(description="Torrent hash")]
    ) -> Any:
        """Get the SSL parameters of a torrent.

        GET /api/v2/torrents/SSLParameters
        """
        return self._call("GET", "torrents/SSLParameters", {"hash": hash})

    def torrents_set_ssl_parameters(
        self,
        *,
        hash: Annotated[str, Field(description="Torrent hash")],
        ssl_certificate: Annotated[str, Field(description="ssl_certificate")],
        ssl_private_key: Annotated[str, Field(description="ssl_private_key")],
        ssl_dh_params: Annotated[str, Field(description="ssl_dh_params")],
    ) -> Any:
        """Set the SSL parameters of a torrent.

        POST /api/v2/torrents/setSSLParameters
        """
        return self._call(
            "POST",
            "torrents/setSSLParameters",
            {
                "hash": hash,
                "ssl_certificate": ssl_certificate,
                "ssl_private_key": ssl_private_key,
                "ssl_dh_params": ssl_dh_params,
            },
        )

    def torrents_fetch_metadata(
        self,
        *,
        source: Annotated[str, Field(description="Magnet link, URL or info-hash")],
        downloader: Annotated[str | None, Field(description="downloader")] = None,
    ) -> Any:
        """Fetch the metadata of a magnet link or URL without adding it.

        POST /api/v2/torrents/fetchMetadata
        """
        return self._call(
            "POST",
            "torrents/fetchMetadata",
            {"source": source, "downloader": downloader},
        )

    def torrents_parse_metadata(
        self,
        *,
        torrent_files: Annotated[
            dict[str, str] | None,
            Field(description="Uploaded .torrent files: file name to base64 content"),
        ] = None,
    ) -> Any:
        """Parse uploaded .torrent files and return their metadata.

        POST /api/v2/torrents/parseMetadata
        """
        return self._call("POST", "torrents/parseMetadata", None, torrent_files)

    def torrents_save_metadata(
        self,
        *,
        source: Annotated[str, Field(description="Magnet link, URL or info-hash")],
    ) -> Any:
        """Save fetched metadata as a .torrent file.

        GET /api/v2/torrents/saveMetadata
        """
        return self._call("GET", "torrents/saveMetadata", {"source": source})


class TransferApi(BaseApiClient):
    """The `transfer` scope of the WebUI API."""

    def transfer_info(self) -> Any:
        """Get global transfer info: speeds, totals, connection status.

        GET /api/v2/transfer/info
        """
        return self._call("GET", "transfer/info")

    def transfer_speed_limits_mode(self) -> Any:
        """Get whether the alternative speed limits are on.

        GET /api/v2/transfer/speedLimitsMode
        """
        return self._call("GET", "transfer/speedLimitsMode")

    def transfer_set_speed_limits_mode(
        self,
        *,
        mode: Annotated[int, Field(description="1 = alternative limits on, 0 = off")],
    ) -> Any:
        """Turn the alternative speed limits on (1) or off (0).

        POST /api/v2/transfer/setSpeedLimitsMode
        """
        return self._call("POST", "transfer/setSpeedLimitsMode", {"mode": mode})

    def transfer_toggle_speed_limits_mode(self) -> Any:
        """Toggle the alternative speed limits.

        POST /api/v2/transfer/toggleSpeedLimitsMode
        """
        return self._call("POST", "transfer/toggleSpeedLimitsMode")

    def transfer_upload_limit(self) -> Any:
        """Get the global upload limit.

        GET /api/v2/transfer/uploadLimit
        """
        return self._call("GET", "transfer/uploadLimit")

    def transfer_download_limit(self) -> Any:
        """Get the global download limit.

        GET /api/v2/transfer/downloadLimit
        """
        return self._call("GET", "transfer/downloadLimit")

    def transfer_set_upload_limit(
        self,
        *,
        limit: Annotated[
            int, Field(description="Limit in bytes per second (0 or -1 = unlimited)")
        ],
    ) -> Any:
        """Set the global upload limit.

        POST /api/v2/transfer/setUploadLimit
        """
        return self._call("POST", "transfer/setUploadLimit", {"limit": limit})

    def transfer_set_download_limit(
        self,
        *,
        limit: Annotated[
            int, Field(description="Limit in bytes per second (0 or -1 = unlimited)")
        ],
    ) -> Any:
        """Set the global download limit.

        POST /api/v2/transfer/setDownloadLimit
        """
        return self._call("POST", "transfer/setDownloadLimit", {"limit": limit})

    def transfer_ban_peers(
        self,
        *,
        peers: Annotated[str, Field(description="Peers as host:port separated by `|`")],
    ) -> Any:
        """Ban peers.

        POST /api/v2/transfer/banPeers
        """
        return self._call("POST", "transfer/banPeers", {"peers": peers})


class Api(
    AppApi,
    ClientDataApi,
    LogApi,
    RssApi,
    SearchApi,
    SyncApi,
    TorrentCreatorApi,
    TorrentsApi,
    TransferApi,
):
    """The qBittorrent WebUI API: every scope in one client."""
