from typing import List, Optional, Dict, Any
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
    locale: Optional[str] = None
    create_subfolder_enabled: Optional[bool] = None
    start_paused_enabled: Optional[bool] = None
    auto_delete_mode: Optional[int] = None
    preallocate_all: Optional[bool] = None
    incomplete_files_ext: Optional[bool] = None
    auto_tmm_enabled: Optional[bool] = None
    torrent_changed_tmm_enabled: Optional[bool] = None
    save_path_changed_tmm_enabled: Optional[bool] = None
    category_changed_tmm_enabled: Optional[bool] = None
    save_path: Optional[str] = None
    temp_path_enabled: Optional[bool] = None
    temp_path: Optional[str] = None
    scan_dirs: Optional[Dict[str, Any]] = None
    export_dir: Optional[str] = None
    export_dir_fin: Optional[str] = None
    mail_notification_enabled: Optional[bool] = None
    mail_notification_sender: Optional[str] = None
    mail_notification_email: Optional[str] = None
    mail_notification_smtp: Optional[str] = None
    mail_notification_ssl_enabled: Optional[bool] = None
    mail_notification_auth_enabled: Optional[bool] = None
    mail_notification_username: Optional[str] = None
    mail_notification_password: Optional[str] = None
    autorun_enabled: Optional[bool] = None
    autorun_program: Optional[str] = None
    queueing_enabled: Optional[bool] = None
    max_active_downloads: Optional[int] = None
    max_active_torrents: Optional[int] = None
    max_active_uploads: Optional[int] = None
    dont_count_slow_torrents: Optional[bool] = None
    slow_torrent_dl_rate_threshold: Optional[int] = None
    slow_torrent_ul_rate_threshold: Optional[int] = None
    slow_torrent_inactive_timer: Optional[int] = None
    max_ratio_enabled: Optional[bool] = None
    max_ratio: Optional[float] = None
    max_ratio_act: Optional[int] = None
    listen_port: Optional[int] = None
    upnp: Optional[bool] = None
    random_port: Optional[bool] = None
    dl_limit: Optional[int] = None
    up_limit: Optional[int] = None
    max_connec: Optional[int] = None
    max_connec_per_torrent: Optional[int] = None
    max_uploads: Optional[int] = None
    max_uploads_per_torrent: Optional[int] = None
    stop_tracker_timeout: Optional[int] = None
    enable_piece_extent_affinity: Optional[bool] = None
    bittorrent_protocol: Optional[int] = None
    limit_utp_rate: Optional[bool] = None
    limit_tcp_overhead: Optional[bool] = None
    limit_lan_peers: Optional[bool] = None
    alt_dl_limit: Optional[int] = None
    alt_up_limit: Optional[int] = None
    scheduler_enabled: Optional[bool] = None
    schedule_from_hour: Optional[int] = None
    schedule_from_min: Optional[int] = None
    schedule_to_hour: Optional[int] = None
    schedule_to_min: Optional[int] = None
    scheduler_days: Optional[int] = None
    dht: Optional[bool] = None
    pex: Optional[bool] = None
    lsd: Optional[bool] = None
    encryption: Optional[int] = None
    anonymous_mode: Optional[bool] = None
    proxy_type: Optional[int] = None
    proxy_ip: Optional[str] = None
    proxy_port: Optional[int] = None
    proxy_peer_connections: Optional[bool] = None
    proxy_auth_enabled: Optional[bool] = None
    proxy_username: Optional[str] = None
    proxy_password: Optional[str] = None
    proxy_torrents_only: Optional[bool] = None
    ip_filter_enabled: Optional[bool] = None
    ip_filter_path: Optional[str] = None
    ip_filter_trackers: Optional[bool] = None
    web_ui_domain_list: Optional[str] = None
    web_ui_address: Optional[str] = None
    web_ui_port: Optional[int] = None
    web_ui_upnp: Optional[bool] = None
    web_ui_username: Optional[str] = None
    web_ui_password: Optional[str] = None
    web_ui_csrf_protection_enabled: Optional[bool] = None
    web_ui_clickjacking_protection_enabled: Optional[bool] = None
    web_ui_secure_cookie_enabled: Optional[bool] = None
    web_ui_max_auth_fail_count: Optional[int] = None
    web_ui_ban_duration: Optional[int] = None
    web_ui_session_timeout: Optional[int] = None
    web_ui_host_header_validation_enabled: Optional[bool] = None
    bypass_local_auth: Optional[bool] = None
    bypass_auth_subnet_whitelist_enabled: Optional[bool] = None
    bypass_auth_subnet_whitelist: Optional[str] = None
    alternative_webui_enabled: Optional[bool] = None
    alternative_webui_path: Optional[str] = None
    use_https: Optional[bool] = None
    web_ui_https_key_path: Optional[str] = None
    web_ui_https_cert_path: Optional[str] = None
    dyndns_enabled: Optional[bool] = None
    dyndns_service: Optional[int] = None
    dyndns_username: Optional[str] = None
    dyndns_password: Optional[str] = None
    dyndns_domain: Optional[str] = None
    rss_refresh_interval: Optional[int] = None
    rss_max_articles_per_feed: Optional[int] = None
    rss_processing_enabled: Optional[bool] = None
    rss_auto_downloading_enabled: Optional[bool] = None
    rss_download_repack_proper_episodes: Optional[bool] = None
    rss_smart_episode_filters: Optional[str] = None
    add_trackers_enabled: Optional[bool] = None
    add_trackers: Optional[str] = None
    web_ui_use_custom_http_headers_enabled: Optional[bool] = None
    web_ui_custom_http_headers: Optional[str] = None
    max_seeding_time_enabled: Optional[bool] = None
    max_seeding_time: Optional[int] = None
    announce_ip: Optional[str] = None
    announce_to_all_tiers: Optional[bool] = None
    announce_to_all_trackers: Optional[bool] = None
    async_io_threads: Optional[int] = None
    banned_IPs: Optional[str] = None
    checking_memory_use: Optional[int] = None
    current_interface_address: Optional[str] = None
    current_network_interface: Optional[str] = None
    disk_cache: Optional[int] = None
    disk_cache_ttl: Optional[int] = None
    embedded_tracker_port: Optional[int] = None
    enable_coalesce_read_write: Optional[bool] = None
    enable_embedded_tracker: Optional[bool] = None
    enable_multi_connections_from_same_ip: Optional[bool] = None
    enable_os_cache: Optional[bool] = None
    enable_upload_suggestions: Optional[bool] = None
    file_pool_size: Optional[int] = None
    outgoing_ports_max: Optional[int] = None
    outgoing_ports_min: Optional[int] = None
    recheck_completed_torrents: Optional[bool] = None
    resolve_peer_countries: Optional[bool] = None
    save_resume_data_interval: Optional[int] = None
    send_buffer_low_watermark: Optional[int] = None
    send_buffer_watermark: Optional[int] = None
    send_buffer_watermark_factor: Optional[int] = None
    socket_backlog_size: Optional[int] = None
    upload_choking_algorithm: Optional[int] = None
    upload_slots_behavior: Optional[int] = None
    upnp_lease_duration: Optional[int] = None
    utp_tcp_mixed_mode: Optional[int] = None


class TorrentInfo(BaseModel):
    added_on: int
    amount_left: int
    auto_tmm: bool
    availability: float
    category: str
    completed: int
    completion_on: int
    content_path: Optional[str] = None
    dl_limit: int
    dlspeed: int
    downloaded: int
    downloaded_session: int
    eta: int
    f_l_piece_prio: bool
    force_start: bool
    hash: str
    isPrivate: Optional[bool] = None
    last_activity: int
    magnet_uri: Optional[str] = None
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
    isPrivate: Optional[bool] = None


class TrackerInfo(BaseModel):
    url: str
    status: int
    tier: int
    num_peers: int
    num_seeds: Optional[int] = None
    num_leeches: Optional[int] = None
    num_downloaded: Optional[int] = None
    msg: str


class WebSeed(BaseModel):
    url: str


class FileInfo(BaseModel):
    index: Optional[int] = None
    name: str
    size: int
    progress: float
    priority: int
    is_seed: bool
    piece_range: List[int]
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
    torrents: Optional[Dict[str, Any]] = None
    torrents_removed: Optional[List[str]] = None
    categories: Optional[Dict[str, Category]] = None
    categories_removed: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    tags_removed: Optional[List[str]] = None
    server_state: Optional[Dict[str, Any]] = None


class TorrentPeers(BaseModel):
    rid: int
    full_update: bool
    peers: Optional[Dict[str, Any]] = None
    peers_removed: Optional[List[str]] = None
    show_flags: bool


class RSSRule(BaseModel):
    enabled: bool
    mustContain: str
    mustNotContain: str
    useRegex: bool
    episodeFilter: str
    smartFilter: bool
    previouslyMatchedEpisodes: List[str]
    affectedFeeds: List[str]
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
    supportedCategories: List[Dict[str, str]]
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
    queueing: Optional[bool] = None
    use_alt_speed_limits: Optional[bool] = None
    refresh_interval: Optional[int] = None
