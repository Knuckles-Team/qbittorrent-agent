"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        "qbittorrent-add-torrent",
        (
            ToolStep(
                "qbittorrent_torrents_categories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_add",
                params=("urls", "category"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_info",
                params=("category",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Add a magnet link or URL the operator asked for into the consuming app's category, and confirm it is listed.",
    ),
    ToolUseContract(
        "qbittorrent-category-roundtrip",
        (
            ToolStep(
                "qbittorrent_torrents_categories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_create_category",
                params=("category",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_categories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_remove_categories",
                params=("categories",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_categories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Create a `zz-validation-<date>` category, confirm it lists, remove it, and confirm it is gone.",
    ),
    ToolUseContract(
        "qbittorrent-check-transfer-health",
        (
            ToolStep(
                "qbittorrent_transfer_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_transfer_speed_limits_mode",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_info",
                params=("filter",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_info",
                params=("filter",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_log_main",
                params=("normal", "info", "warning", "critical"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read the connection status, speeds and limits, and list stalled and errored torrents with the log reasons.",
    ),
    ToolUseContract(
        "qbittorrent-diagnose-app-connection",
        (
            ToolStep(
                "qbittorrent_log_main",
                params=("normal", "info", "warning", "critical"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_preferences",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_categories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="When an arr app reports its qBittorrent client unavailable, read the login failures and bans in the log and the WebUI auth settings, then hand the fix to the arr-mcp `arr-repair-download-client` workflow.",
    ),
    ToolUseContract(
        "qbittorrent-ingest-torrents",
        (
            ToolStep(
                "qbittorrent_torrents_count",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_ingest_torrents",
                params=("filter",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Count the torrents and push them, with trackers and categories, into the knowledge graph.",
    ),
    ToolUseContract(
        "qbittorrent-provision-app-category",
        (
            ToolStep(
                "qbittorrent_torrents_categories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_default_save_path",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_create_category",
                params=("category",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_categories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Create the category an arr app sends its downloads to, so they land in the app's import folder.",
    ),
    ToolUseContract(
        "qbittorrent-recover-stalled-torrent",
        (
            ToolStep(
                "qbittorrent_torrents_info",
                params=("filter",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_trackers",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_reannounce",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_recheck",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_properties",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="For one stalled torrent, read its trackers, reannounce, and recheck it if its data may be damaged.",
    ),
    ToolUseContract(
        "qbittorrent-set-share-limits",
        (
            ToolStep(
                "qbittorrent_torrents_info",
                params=("filter",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_properties",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_share_limits",
                params=(
                    "hashes",
                    "ratio_limit",
                    "seeding_time_limit",
                    "inactive_seeding_time_limit",
                    "share_limit_action",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_properties",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read completed torrents' ratio and seeding time, and set their share limits with approval.",
    ),
    ToolUseContract(
        "qbittorrent-set-speed-limits",
        (
            ToolStep(
                "qbittorrent_transfer_download_limit",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_transfer_upload_limit",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_transfer_set_download_limit",
                params=("limit",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_transfer_set_upload_limit",
                params=("limit",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_transfer_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and set the global download and upload limits with approval.",
    ),
    ToolUseContract(
        "qbittorrent-manage-app",
        (
            ToolStep(
                "qbittorrent_app_build_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_cookies",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_get_directory_content",
                params=("dir_path", "mode", "with_metadata"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_network_interface_address_list",
                params=("iface",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_network_interface_list",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_process_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_version",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_webapi_version",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_delete_api_key",
                params=("confirm",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_rotate_api_key",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_send_test_email",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_set_cookies",
                params=("cookies",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_set_preferences",
                params=("preferences",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_app_shutdown",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change app on qbittorrent through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "qbittorrent-manage-clientdata",
        (
            ToolStep(
                "qbittorrent_clientdata_load",
                params=("keys",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_clientdata_store",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
        ),
        description="Read and change clientdata on qbittorrent through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "qbittorrent-manage-log",
        (
            ToolStep(
                "qbittorrent_log_peers",
                params=("last_known_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change log on qbittorrent through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "qbittorrent-manage-rss",
        (
            ToolStep(
                "qbittorrent_rss_items",
                params=("with_data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_matching_articles",
                params=("rule_name",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_rules",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_set_feed_refresh_interval",
                params=("path", "refresh_interval"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_add_feed",
                params=("path", "refresh_interval", "url"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_add_folder",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_mark_as_read",
                params=("article_id", "item_path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_move_item",
                params=("dest_path", "item_path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_refresh_item",
                params=("item_path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_remove_item",
                params=("confirm", "path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_remove_rule",
                params=("confirm", "rule_name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_rename_rule",
                params=("new_rule_name", "rule_name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_set_feed_url",
                params=("path", "url"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_rss_set_rule",
                params=("rule_def", "rule_name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change rss on qbittorrent through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "qbittorrent-manage-search",
        (
            ToolStep(
                "qbittorrent_search_download_torrent",
                params=("plugin_name", "torrent_url"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_plugins",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_results",
                params=("id", "limit", "offset"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_status",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_delete",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_enable_plugin",
                params=("enable", "names"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_install_plugin",
                params=("sources",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_start",
                params=("category", "pattern", "plugins"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_stop",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_uninstall_plugin",
                params=("names",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_search_update_plugins",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change search on qbittorrent through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "qbittorrent-manage-sync",
        (
            ToolStep(
                "qbittorrent_sync_maindata",
                params=("rid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_sync_torrent_peers",
                params=("hash", "rid"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change sync on qbittorrent through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "qbittorrent-manage-torrentcreator",
        (
            ToolStep(
                "qbittorrent_torrentcreator_status",
                params=("task_i_d",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrentcreator_torrent_file",
                params=("task_i_d",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrentcreator_add_task",
                params=(
                    "comment",
                    "format",
                    "optimize_alignment",
                    "padded_file_size_limit",
                    "piece_size",
                    "private",
                    "source",
                    "source_path",
                    "start_seeding",
                    "torrent_file_path",
                    "trackers",
                    "url_seeds",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrentcreator_delete_task",
                params=("confirm", "task_i_d"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change torrentcreator on qbittorrent through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "qbittorrent-manage-torrents",
        (
            ToolStep(
                "qbittorrent_torrents_download_limit",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_export",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_files",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_piece_availability",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_piece_hashes",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_piece_states",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_save_metadata",
                params=("source",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_ssl_parameters",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_tags",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_upload_limit",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_webseeds",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_add_peers",
                params=("hashes", "peers"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_add_tags",
                params=("hashes", "tags"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_add_trackers",
                params=("hash", "urls"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_add_web_seeds",
                params=("hash", "urls"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_bottom_prio",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_create_tags",
                params=("tags",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_decrease_prio",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_delete",
                params=("confirm", "delete_files", "hashes"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_delete_tags",
                params=("confirm", "tags"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_edit_category",
                params=(
                    "category",
                    "download_path",
                    "download_path_enabled",
                    "save_path",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_edit_tracker",
                params=("hash", "new_url", "tier", "url"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_edit_web_seed",
                params=("hash", "new_url", "orig_url"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_fetch_metadata",
                params=("downloader", "source"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_file_prio",
                params=("hash", "id", "priority"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_increase_prio",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_parse_metadata",
                params=("torrent_files",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_remove_tags",
                params=("confirm", "hashes", "tags"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_remove_trackers",
                params=("confirm", "hash", "urls"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_remove_web_seeds",
                params=("confirm", "hash", "urls"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_rename",
                params=("hash", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_rename_file",
                params=("hash", "new_path", "old_path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_rename_folder",
                params=("hash", "new_path", "old_path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_auto_management",
                params=("enable", "hashes"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_category",
                params=("category", "hashes"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_comment",
                params=("comment", "hashes"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "UNSUPPORTED_BY_SERVER",
                        "the server runs a qBittorrent release older than 5.2",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_download_limit",
                params=("hashes", "limit"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_download_path",
                params=("id", "path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_force_start",
                params=("hashes", "value"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_location",
                params=("hashes", "location"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_save_path",
                params=("id", "path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_ssl_parameters",
                params=("hash", "ssl_certificate", "ssl_dh_params", "ssl_private_key"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_super_seeding",
                params=("hashes", "value"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_tags",
                params=("hashes", "tags"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_set_upload_limit",
                params=("hashes", "limit"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_start",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_stop",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_toggle_first_last_piece_prio",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_toggle_sequential_download",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_torrents_top_prio",
                params=("hashes",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change torrents on qbittorrent through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "qbittorrent-manage-transfer",
        (
            ToolStep(
                "qbittorrent_transfer_ban_peers",
                params=("peers",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_transfer_set_speed_limits_mode",
                params=("mode",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "qbittorrent_transfer_toggle_speed_limits_mode",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change transfer on qbittorrent through its typed tools, reading before any write.",
    ),
)

LINKS = (
    SurfaceLink(
        "qbittorrent-add-torrent",
        tools=(
            "qbittorrent_torrents_add",
            "qbittorrent_torrents_categories",
            "qbittorrent_torrents_info",
        ),
        prompts=("torrent_operator",),
        skills=("qbittorrent-torrent-lifecycle",),
    ),
    SurfaceLink(
        "qbittorrent-category-roundtrip",
        tools=(
            "qbittorrent_torrents_categories",
            "qbittorrent_torrents_create_category",
            "qbittorrent_torrents_remove_categories",
        ),
        prompts=("download_client_steward", "torrent_operator"),
        skills=("qbittorrent-torrent-lifecycle",),
    ),
    SurfaceLink(
        "qbittorrent-check-transfer-health",
        tools=(
            "qbittorrent_log_main",
            "qbittorrent_torrents_info",
            "qbittorrent_transfer_info",
            "qbittorrent_transfer_speed_limits_mode",
        ),
        prompts=("seeding_manager", "torrent_download_monitor", "torrent_operator"),
        skills=("qbittorrent-transfer-tuning",),
    ),
    SurfaceLink(
        "qbittorrent-diagnose-app-connection",
        tools=(
            "qbittorrent_app_preferences",
            "qbittorrent_log_main",
            "qbittorrent_torrents_categories",
        ),
        prompts=("download_client_steward", "torrent_operator"),
        skills=("qbittorrent-download-client",),
    ),
    SurfaceLink(
        "qbittorrent-ingest-torrents",
        tools=(
            "qbittorrent_ingest_torrents",
            "qbittorrent_torrents_count",
        ),
        prompts=("torrent_operator",),
        skills=("qbittorrent-kg-ingestion",),
    ),
    SurfaceLink(
        "qbittorrent-provision-app-category",
        tools=(
            "qbittorrent_app_default_save_path",
            "qbittorrent_torrents_categories",
            "qbittorrent_torrents_create_category",
        ),
        prompts=("download_client_steward", "torrent_operator"),
        skills=("qbittorrent-download-client",),
    ),
    SurfaceLink(
        "qbittorrent-recover-stalled-torrent",
        tools=(
            "qbittorrent_torrents_info",
            "qbittorrent_torrents_properties",
            "qbittorrent_torrents_reannounce",
            "qbittorrent_torrents_recheck",
            "qbittorrent_torrents_trackers",
        ),
        prompts=("torrent_download_monitor", "torrent_operator"),
        skills=("qbittorrent-torrent-lifecycle",),
    ),
    SurfaceLink(
        "qbittorrent-set-share-limits",
        tools=(
            "qbittorrent_torrents_info",
            "qbittorrent_torrents_properties",
            "qbittorrent_torrents_set_share_limits",
        ),
        prompts=("seeding_manager", "torrent_operator"),
        skills=("qbittorrent-transfer-tuning",),
    ),
    SurfaceLink(
        "qbittorrent-set-speed-limits",
        tools=(
            "qbittorrent_transfer_download_limit",
            "qbittorrent_transfer_info",
            "qbittorrent_transfer_set_download_limit",
            "qbittorrent_transfer_set_upload_limit",
            "qbittorrent_transfer_upload_limit",
        ),
        prompts=("seeding_manager", "torrent_operator"),
        skills=("qbittorrent-transfer-tuning",),
    ),
    SurfaceLink(
        "qbittorrent-manage-app",
        tools=(
            "qbittorrent_app_build_info",
            "qbittorrent_app_cookies",
            "qbittorrent_app_delete_api_key",
            "qbittorrent_app_get_directory_content",
            "qbittorrent_app_network_interface_address_list",
            "qbittorrent_app_network_interface_list",
            "qbittorrent_app_process_info",
            "qbittorrent_app_rotate_api_key",
            "qbittorrent_app_send_test_email",
            "qbittorrent_app_set_cookies",
            "qbittorrent_app_set_preferences",
            "qbittorrent_app_shutdown",
            "qbittorrent_app_version",
            "qbittorrent_app_webapi_version",
        ),
        prompts=("torrent_operator",),
        skills=("qbittorrent-agent-operations",),
    ),
    SurfaceLink(
        "qbittorrent-manage-clientdata",
        tools=(
            "qbittorrent_clientdata_load",
            "qbittorrent_clientdata_store",
        ),
        prompts=("torrent_operator",),
        skills=("qbittorrent-agent-operations",),
    ),
    SurfaceLink(
        "qbittorrent-manage-log",
        tools=("qbittorrent_log_peers",),
        prompts=("torrent_operator",),
        skills=("qbittorrent-agent-operations",),
    ),
    SurfaceLink(
        "qbittorrent-manage-rss",
        tools=(
            "qbittorrent_rss_add_feed",
            "qbittorrent_rss_add_folder",
            "qbittorrent_rss_items",
            "qbittorrent_rss_mark_as_read",
            "qbittorrent_rss_matching_articles",
            "qbittorrent_rss_move_item",
            "qbittorrent_rss_refresh_item",
            "qbittorrent_rss_remove_item",
            "qbittorrent_rss_remove_rule",
            "qbittorrent_rss_rename_rule",
            "qbittorrent_rss_rules",
            "qbittorrent_rss_set_feed_refresh_interval",
            "qbittorrent_rss_set_feed_url",
            "qbittorrent_rss_set_rule",
        ),
        prompts=(
            "torrent_operator",
            "download_client_steward",
            "torrent_download_monitor",
        ),
        skills=("qbittorrent-torrent-lifecycle",),
    ),
    SurfaceLink(
        "qbittorrent-manage-search",
        tools=(
            "qbittorrent_search_delete",
            "qbittorrent_search_download_torrent",
            "qbittorrent_search_enable_plugin",
            "qbittorrent_search_install_plugin",
            "qbittorrent_search_plugins",
            "qbittorrent_search_results",
            "qbittorrent_search_start",
            "qbittorrent_search_status",
            "qbittorrent_search_stop",
            "qbittorrent_search_uninstall_plugin",
            "qbittorrent_search_update_plugins",
        ),
        prompts=(
            "torrent_operator",
            "download_client_steward",
            "torrent_download_monitor",
        ),
        skills=("qbittorrent-torrent-lifecycle",),
    ),
    SurfaceLink(
        "qbittorrent-manage-sync",
        tools=(
            "qbittorrent_sync_maindata",
            "qbittorrent_sync_torrent_peers",
        ),
        prompts=("torrent_operator", "seeding_manager", "torrent_download_monitor"),
        skills=("qbittorrent-transfer-tuning",),
    ),
    SurfaceLink(
        "qbittorrent-manage-torrentcreator",
        tools=(
            "qbittorrent_torrentcreator_add_task",
            "qbittorrent_torrentcreator_delete_task",
            "qbittorrent_torrentcreator_status",
            "qbittorrent_torrentcreator_torrent_file",
        ),
        prompts=(
            "torrent_operator",
            "download_client_steward",
            "torrent_download_monitor",
        ),
        skills=("qbittorrent-torrent-lifecycle",),
    ),
    SurfaceLink(
        "qbittorrent-manage-torrents",
        tools=(
            "qbittorrent_torrents_add_peers",
            "qbittorrent_torrents_add_tags",
            "qbittorrent_torrents_add_trackers",
            "qbittorrent_torrents_add_web_seeds",
            "qbittorrent_torrents_bottom_prio",
            "qbittorrent_torrents_create_tags",
            "qbittorrent_torrents_decrease_prio",
            "qbittorrent_torrents_delete",
            "qbittorrent_torrents_delete_tags",
            "qbittorrent_torrents_download_limit",
            "qbittorrent_torrents_edit_category",
            "qbittorrent_torrents_edit_tracker",
            "qbittorrent_torrents_edit_web_seed",
            "qbittorrent_torrents_export",
            "qbittorrent_torrents_fetch_metadata",
            "qbittorrent_torrents_file_prio",
            "qbittorrent_torrents_files",
            "qbittorrent_torrents_increase_prio",
            "qbittorrent_torrents_parse_metadata",
            "qbittorrent_torrents_piece_availability",
            "qbittorrent_torrents_piece_hashes",
            "qbittorrent_torrents_piece_states",
            "qbittorrent_torrents_remove_tags",
            "qbittorrent_torrents_remove_trackers",
            "qbittorrent_torrents_remove_web_seeds",
            "qbittorrent_torrents_rename",
            "qbittorrent_torrents_rename_file",
            "qbittorrent_torrents_rename_folder",
            "qbittorrent_torrents_save_metadata",
            "qbittorrent_torrents_set_auto_management",
            "qbittorrent_torrents_set_category",
            "qbittorrent_torrents_set_comment",
            "qbittorrent_torrents_set_download_limit",
            "qbittorrent_torrents_set_download_path",
            "qbittorrent_torrents_set_force_start",
            "qbittorrent_torrents_set_location",
            "qbittorrent_torrents_set_save_path",
            "qbittorrent_torrents_set_ssl_parameters",
            "qbittorrent_torrents_set_super_seeding",
            "qbittorrent_torrents_set_tags",
            "qbittorrent_torrents_set_upload_limit",
            "qbittorrent_torrents_ssl_parameters",
            "qbittorrent_torrents_start",
            "qbittorrent_torrents_stop",
            "qbittorrent_torrents_tags",
            "qbittorrent_torrents_toggle_first_last_piece_prio",
            "qbittorrent_torrents_toggle_sequential_download",
            "qbittorrent_torrents_top_prio",
            "qbittorrent_torrents_upload_limit",
            "qbittorrent_torrents_webseeds",
        ),
        prompts=(
            "torrent_operator",
            "download_client_steward",
            "torrent_download_monitor",
        ),
        skills=("qbittorrent-torrent-lifecycle",),
    ),
    SurfaceLink(
        "qbittorrent-manage-transfer",
        tools=(
            "qbittorrent_transfer_ban_peers",
            "qbittorrent_transfer_set_speed_limits_mode",
            "qbittorrent_transfer_toggle_speed_limits_mode",
        ),
        prompts=("torrent_operator", "seeding_manager", "torrent_download_monitor"),
        skills=("qbittorrent-transfer-tuning",),
    ),
)

LOCATIONS = (
    DataLocation(
        "qbittorrent-torrents",
        ("Torrent",),
        "QBITTORRENT_URL",
        "qbittorrent_torrents_info",
    ),
    DataLocation(
        "qbittorrent-categories",
        ("ClientCategory",),
        "QBITTORRENT_URL",
        "qbittorrent_torrents_categories",
    ),
    DataLocation(
        "qbittorrent-instance",
        ("ClientInstance",),
        "QBITTORRENT_URL",
        "qbittorrent_transfer_info",
    ),
    DataLocation(
        "qbittorrent-feeds",
        ("RssFeedItem",),
        "QBITTORRENT_URL",
        "qbittorrent_rss_items",
    ),
)

ROLES = (
    BusinessRole(
        "download client steward",
        tasks=(
            "qbittorrent-category-roundtrip",
            "qbittorrent-diagnose-app-connection",
            "qbittorrent-manage-rss",
            "qbittorrent-manage-search",
            "qbittorrent-manage-torrentcreator",
            "qbittorrent-manage-torrents",
            "qbittorrent-provision-app-category",
        ),
    ),
    BusinessRole(
        "seeding manager",
        tasks=(
            "qbittorrent-check-transfer-health",
            "qbittorrent-manage-sync",
            "qbittorrent-manage-transfer",
            "qbittorrent-set-share-limits",
            "qbittorrent-set-speed-limits",
        ),
    ),
    BusinessRole(
        "torrent download monitor",
        tasks=(
            "qbittorrent-check-transfer-health",
            "qbittorrent-manage-rss",
            "qbittorrent-manage-search",
            "qbittorrent-manage-sync",
            "qbittorrent-manage-torrentcreator",
            "qbittorrent-manage-torrents",
            "qbittorrent-manage-transfer",
            "qbittorrent-recover-stalled-torrent",
        ),
    ),
)
