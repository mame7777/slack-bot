# slack-bot
Slackワークスペース内の公開チャンネルの投稿を取得し，一つのチャンネルに同じ内容を投稿するbotです．  
  
※ファイルや画像の投稿は都合により非対応です．  
  

# 構築方法など
## botに必要な権限
[slack apiのページ](https://api.slack.com/apps)内の自分のアプリから以下の設定する．  
  
### Settings > Basic Information
App-Level Tokensに以下のスコープを追加．  
このときのトークンは後で使う．  
- connections:write 
  
### Settings > Socket Mode
Enableにする．  
  
### Features > OAuth & Permissions
ScopesのBot Token Scopesから以下のOAuth Scopeを追加．
- app_mentions:read
- channels:history
- channels:join
- channels:read
- chat:write
- chat:write.customize
- users:read
  
### Features > Event Subscriptions
Enable EventsをEnableにする．  
Subscribe to events on behalf of usersにて，以下のEvent Nameを追加．  
- message.channels
- app_mention

## 環境構築
1. 上記のslack apiのページの「Bot User OAuth Token」を"SLACK_BOT_TOKEN"，「App-level Token」を"SLACK_APP_TOKEN"として，本ディレクトリ内に作成した「.env」ファイルに記載．  
1. requirements.txtを用いて，ライブラリ類のインストールする．  
1. src/main.py内のPOST_CHANNEL_NAMEに，投稿したいchannel名を指定する．
1. 実行する．