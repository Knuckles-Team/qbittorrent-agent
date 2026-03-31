from typing import List, Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class AppPreferences(BaseModel):

    save_path: Optional[str] = None
    temp_path: Optional[str] = None
    auto_tmm_enabled: Optional[bool] = None
    torrent_changed_tmm_enabled: Optional[bool] = None
    save_path_changed_tmm_enabled: Optional[bool] = None
    category_changed_tmm_enabled: Optional[bool] = None


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


class Category(BaseModel):
    name: str
    savePath: str


class RSSItem(BaseModel):

    pass


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


class TransferInfo(BaseModel):
    dl_info_speed: int
    dl_info_data: int
    up_info_speed: int
    up_info_data: int
    dl_rate_limit: int
    up_rate_limit: int
    dht_nodes: int
    connection_status: str
