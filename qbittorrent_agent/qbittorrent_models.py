from typing import Any

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class BuildInfo(BaseModel):
    qt: str
    libtorrent: str
    boost: str
    openssl: str
    bitness: int


class AppPreferences(BaseModel):
    locale: str | None = None
    create_subfolder_enabled: bool | None = None
    start_paused_enabled: bool | None = None
    auto_delete_mode: int | None = None
    preallocate_all: bool | None = None
    incomplete_files_ext: bool | None = None
    auto_tmm_enabled: bool | None = None
    torrent_changed_tmm_enabled: bool | None = None
    save_path_changed_tmm_enabled: bool | None = None
    category_changed_tmm_enabled: bool | None = None
    save_path: str | None = None
    temp_path_enabled: bool | None = None
    temp_path: str | None = None
    scan_dirs: dict[str, Any] | None = None
    export_dir: str | None = None
    export_dir_fin: str | None = None
    mail_notification_enabled: bool | None = None
    mail_notification_sender: str | None = None
    mail_notification_email: str | None = None
    mail_notification_smtp: str | None = None
    mail_notification_ssl_enabled: bool | None = None
    mail_notification_auth_enabled: bool | None = None
    mail_notification_username: str | None = None
    mail_notification_password: str | None = None
    autorun_enabled: bool | None = None
    autorun_program: str | None = None
    queueing_enabled: bool | None = None
    max_active_downloads: int | None = None
    max_active_torrents: int | None = None
    max_active_uploads: int | None = None
    dont_count_slow_torrents: bool | None = None
    slow_torrent_dl_rate_threshold: int | None = None
    slow_torrent_ul_rate_threshold: int | None = None
    slow_torrent_inactive_timer: int | None = None
    max_ratio_enabled: bool | None = None
    max_ratio: float | None = None
    max_ratio_act: int | None = None
    listen_port: int | None = None
    upnp: bool | None = None
    random_port: bool | None = None
    dl_limit: int | None = None
    up_limit: int | None = None
    max_connec: int | None = None
    max_connec_per_torrent: int | None = None
    max_uploads: int | None = None
    max_uploads_per_torrent: int | None = None
    stop_tracker_timeout: int | None = None
    enable_piece_extent_affinity: bool | None = None
    bittorrent_protocol: int | None = None
    limit_utp_rate: bool | None = None
    limit_tcp_overhead: bool | None = None
    limit_lan_peers: bool | None = None
    alt_dl_limit: int | None = None
    alt_up_limit: int | None = None
    scheduler_enabled: bool | None = None
    schedule_from_hour: int | None = None
    schedule_from_min: int | None = None
    schedule_to_hour: int | None = None
    schedule_to_min: int | None = None
    scheduler_days: int | None = None
    dht: bool | None = None
    pex: bool | None = None
    lsd: bool | None = None
    encryption: int | None = None
    anonymous_mode: bool | None = None
    proxy_type: int | None = None
    proxy_ip: str | None = None
    proxy_port: int | None = None
    proxy_peer_connections: bool | None = None
    proxy_auth_enabled: bool | None = None
    proxy_username: str | None = None
    proxy_password: str | None = None
    proxy_torrents_only: bool | None = None
    ip_filter_enabled: bool | None = None
    ip_filter_path: str | None = None
    ip_filter_trackers: bool | None = None
    web_ui_domain_list: str | None = None
    web_ui_address: str | None = None
    web_ui_port: int | None = None
    web_ui_upnp: bool | None = None
    web_ui_username: str | None = None
    web_ui_password: str | None = None
    web_ui_csrf_protection_enabled: bool | None = None
    web_ui_clickjacking_protection_enabled: bool | None = None
    web_ui_secure_cookie_enabled: bool | None = None
    web_ui_max_auth_fail_count: int | None = None
    web_ui_ban_duration: int | None = None
    web_ui_session_timeout: int | None = None
    web_ui_host_header_validation_enabled: bool | None = None
    bypass_local_auth: bool | None = None
    bypass_auth_subnet_whitelist_enabled: bool | None = None
    bypass_auth_subnet_whitelist: str | None = None
    alternative_webui_enabled: bool | None = None
    alternative_webui_path: str | None = None
    use_https: bool | None = None
    web_ui_https_key_path: str | None = None
    web_ui_https_cert_path: str | None = None
    dyndns_enabled: bool | None = None
    dyndns_service: int | None = None
    dyndns_username: str | None = None
    dyndns_password: str | None = None
    dyndns_domain: str | None = None
    rss_refresh_interval: int | None = None
    rss_max_articles_per_feed: int | None = None
    rss_processing_enabled: bool | None = None
    rss_auto_downloading_enabled: bool | None = None
    rss_download_repack_proper_episodes: bool | None = None
    rss_smart_episode_filters: str | None = None
    add_trackers_enabled: bool | None = None
    add_trackers: str | None = None
    web_ui_use_custom_http_headers_enabled: bool | None = None
    web_ui_custom_http_headers: str | None = None
    max_seeding_time_enabled: bool | None = None
    max_seeding_time: int | None = None
    announce_ip: str | None = None
    announce_to_all_tiers: bool | None = None
    announce_to_all_trackers: bool | None = None
    async_io_threads: int | None = None
    banned_IPs: str | None = None
    checking_memory_use: int | None = None
    current_interface_address: str | None = None
    current_network_interface: str | None = None
    disk_cache: int | None = None
    disk_cache_ttl: int | None = None
    embedded_tracker_port: int | None = None
    enable_coalesce_read_write: bool | None = None
    enable_embedded_tracker: bool | None = None
    enable_multi_connections_from_same_ip: bool | None = None
    enable_os_cache: bool | None = None
    enable_upload_suggestions: bool | None = None
    file_pool_size: int | None = None
    outgoing_ports_max: int | None = None
    outgoing_ports_min: int | None = None
    recheck_completed_torrents: bool | None = None
    resolve_peer_countries: bool | None = None
    save_resume_data_interval: int | None = None
    send_buffer_low_watermark: int | None = None
    send_buffer_watermark: int | None = None
    send_buffer_watermark_factor: int | None = None
    socket_backlog_size: int | None = None
    upload_choking_algorithm: int | None = None
    upload_slots_behavior: int | None = None
    upnp_lease_duration: int | None = None
    utp_tcp_mixed_mode: int | None = None


class TorrentInfo(BaseModel):
    added_on: int
    amount_left: int
    auto_tmm: bool
    availability: float
    category: str
    completed: int
    completion_on: int
    content_path: str | None = None
    dl_limit: int
    dlspeed: int
    downloaded: int
    downloaded_session: int
    eta: int
    f_l_piece_prio: bool
    force_start: bool
    hash: str
    isPrivate: bool | None = None
    last_activity: int
    magnet_uri: str | None = None
    max_ratio: float
    max_seeding_time: int
    name: str
    num_complete: int
    num_incomplete: int
    num_leechs: int
    num_seeds: int
    priority: int
    progress: float
    ratio: float
    ratio_limit: float
    save_path: str
    seeding_time: int
    seeding_time_limit: int
    seen_complete: int
    seq_dl: bool
    size: int
    state: str
    super_seeding: bool
    tags: str
    time_active: int
    total_size: int
    tracker: str
    up_limit: int
    uploaded: int
    uploaded_session: int
    upspeed: int


class TorrentProperties(BaseModel):
    save_path: str
    creation_date: int
    piece_size: int
    comment: str
    total_wasted: int
    total_uploaded: int
    total_uploaded_session: int
    total_downloaded: int
    total_downloaded_session: int
    up_limit: int
    dl_limit: int
    time_elapsed: int
    seeding_time: int
    nb_connections: int
    nb_connections_limit: int
    share_ratio: float
    addition_date: int
    completion_date: int
    created_by: str
    dl_speed_avg: int
    dl_speed: int
    eta: int
    last_seen: int
    peers: int
    peers_total: int
    pieces_have: int
    pieces_num: int
    reannounce: int
    seeds: int
    seeds_total: int
    total_size: int
    up_speed_avg: int
    up_speed: int
    isPrivate: bool | None = None


class TrackerInfo(BaseModel):
    url: str
    status: int
    tier: int
    num_peers: int
    num_seeds: int | None = None
    num_leeches: int | None = None
    num_downloaded: int | None = None
    msg: str


class WebSeed(BaseModel):
    url: str


class FileInfo(BaseModel):
    index: int | None = None
    name: str
    size: int
    progress: float
    priority: int
    is_seed: bool
    piece_range: list[int]
    availability: float


class Category(BaseModel):
    name: str
    savePath: str


class Tag(BaseModel):
    name: str


class LogEntry(BaseModel):
    id: int
    message: str
    timestamp: int
    type: int


class PeerLogEntry(BaseModel):
    id: int
    ip: str
    timestamp: int
    blocked: bool
    reason: str


class MainData(BaseModel):
    rid: int
    full_update: bool
    torrents: dict[str, Any] | None = None
    torrents_removed: list[str] | None = None
    categories: dict[str, Category] | None = None
    categories_removed: list[str] | None = None
    tags: list[str] | None = None
    tags_removed: list[str] | None = None
    server_state: dict[str, Any] | None = None


class TorrentPeers(BaseModel):
    rid: int
    full_update: bool
    peers: dict[str, Any] | None = None
    peers_removed: list[str] | None = None
    show_flags: bool


class RSSRule(BaseModel):
    enabled: bool
    mustContain: str
    mustNotContain: str
    useRegex: bool
    episodeFilter: str
    smartFilter: bool
    previouslyMatchedEpisodes: list[str]
    affectedFeeds: list[str]
    ignoreDays: int
    lastMatch: str
    addPaused: bool
    assignedCategory: str
    savePath: str


class SearchJob(BaseModel):
    id: int


class SearchStatus(BaseModel):
    id: int
    status: str
    total: int


class SearchResult(BaseModel):
    descrLink: str
    fileName: str
    fileSize: int
    fileUrl: str
    nbLeechers: int
    nbSeeders: int
    siteUrl: str


class SearchPlugin(BaseModel):
    enabled: bool
    fullName: str
    name: str
    supportedCategories: list[dict[str, str]]
    url: str
    version: str


class TransferInfo(BaseModel):
    dl_info_speed: int
    dl_info_data: int
    up_info_speed: int
    up_info_data: int
    dl_rate_limit: int
    up_rate_limit: int
    dht_nodes: int
    connection_status: str
    queueing: bool | None = None
    use_alt_speed_limits: bool | None = None
    refresh_interval: int | None = None
