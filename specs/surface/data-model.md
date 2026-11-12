# CONN-QBITTORRENT-AGENT-SURFACE — Data model

The ontology namespace is `https://knuckles-team.github.io/ontology/connector/qbittorrent#` (`qbt:`). The core namespace is `https://knuckles-team.github.io/ontology/core#` (`:`).

| Class | Core parent |
|---|---|
| `qbt:TorrentClientApp` | `:Application` |
| `qbt:ClientInstance` | `:AssetInstance` |
| `qbt:SavePath` | `:Folder` |
| `qbt:ClientCategory` | `:Category` |
| `qbt:ClientTag` | `:Tag` |
| `qbt:RssFeedItem` | `:Feed` |
| `qbt:RssDownloadRule` | `:Policy` |
| `qbt:SearchEnginePlugin` | `:SoftwareComponent` |
| `qbt:RoutingRule` | `:Policy` |
| `qbt:FederationLink` | `:ConfigurationItemCollection` |
| `qbt:ConnectorTool` | `:Tool` |
| `qbt:ToolUseContract` | `:Procedure` |
| `qbt:ContractStep` | `:TaskStep` |
| `qbt:ParameterBinding` | `:ActionParameter` |
| `qbt:ConnectorSkill` | `:Procedure` |
| `qbt:ConnectorPrompt` | `:Prompt` |
| `qbt:TorrentAgentRole` | `:Role` |
| `qbt:TorrentOperator`, `qbt:TorrentDownloadMonitor`, `qbt:SeedingManager`, `qbt:DownloadClientSteward` | `qbt:TorrentAgentRole` |

Ingest emits the core classes `:Torrent`, `:Tracker` and `:Category`.
