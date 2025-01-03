mapping = {
    "com.hyphenate": "io.agora",
    "internal.com.getkeepsafe.relinker": "inner.com.getkeepsafe.relinker",
    "EMClient": "ChatClient",
    "EMOptions": "ChatOptions",
    "EMCallBack": "CallBack",
    "EMResultCallBack": "ResultCallBack",
    "EMChatRoomChangeListener": "ChatRoomChangeListener",
    "EMClientListener": "ChatClientListener",
    "EMConnectionListener": "ConnectionListener",
    "EMConversationListener": "ConversationListener",
    "EMContactListener": "ContactListener",
    "EMError": "Error",
    "EMGroupChangeListener": "GroupChangeListener",
    "EMMessageListener": "MessageListener",
    "EMMultiDeviceListener": "MultiDeviceListener",
    "EMValueCallBack": "ValueCallBack",
    "EMChatManager": "ChatManager",
    "EMChatRoom": "ChatRoom",
    "EMChatRoomManager": "ChatRoomManager",
    "EMCheckType": "ChatCheckType",
    "EMCmdMessageBody": "CmdMessageBody",
    "EMContactManager": "ContactManager",
    "EMConversation": "Conversation",
    "EMConversationType": "ConversationType",
    "EMSearchDirection": "SearchDirection",
    "EMCursorResult": "CursorResult",
    "EMCustomMessageBody": "CustomMessageBody",
    "EMDeviceInfo": "DeviceInfo",
    "EMFileMessageBody": "FileMessageBody",
    "EMGroup": "Group",
    "EMGroupInfo": "GroupInfo",
    "EMGroupManager": "GroupManager",
    "EMGroupOptions": "GroupOptions",
    "EMGroupReadAck": "GroupReadAck",
    "EMImageMessageBody": "ImageMessageBody",
    "EMLocationMessageBody": "LocationMessageBody",
    "EMMessageBody": "MessageBody",
    "EMMucSharedFile": "MucSharedFile",
    "EMNormalFileMessageBody": "NormalFileMessageBody",
    "EMPageResult": "PageResult",
    "EMPushConfigs": "PushConfigs",
    "EMPushManager": "PushManager",
    "EMTextMessageBody": "TextMessageBody",
    "EMCombineMessageBody": "CombineMessageBody",
    "EMUserInfo": "UserInfo",
    "EMUserInfoType": "UserInfoType",
    "EMUserInfoManager": "UserInfoManager",
    "EMVideoMessageBody": "VideoMessageBody",
    "EMVoiceMessageBody": "VoiceMessageBody",
    "HyphenateException": "ChatException",
    "EMPushConfig": "PushConfig",
    "EMPushHelper": "PushHelper",
    "EMPushType": "PushType",
    "EMFileHelper": "FileHelper",
    "EMGroupPermissionType": "GroupPermissionType",
    "EMGroupStyle": "GroupStyle",
    "EMGroupStylePrivateOnlyOwnerInvite": "GroupStylePrivateOnlyOwnerInvite",
    "EMGroupStylePrivateMemberCanInvite": "GroupStylePrivateMemberCanInvite",
    "EMGroupStylePublicJoinNeedApproval": "GroupStylePublicJoinNeedApproval",
    "EMGroupStylePublicJoinNeedApproval": "GroupStylePublicJoinNeedApproval",
    "EMChatRoomPermissionType": "ChatRoomPermissionType",
    "EMChatService": "ChatService",
    "EMJobService": "ChatJobService",
    "EMMonitorReceiver": "MonitorReceiver",
    "EMMzMsgReceiver": "MzMsgReceiver",
    "EMVivoMsgReceiver": "VivoMsgReceiver",
    "EMLanguage": "Language",
    "EMTranslateParams": "TranslateParams",
    "EMTranslationManager": "TranslationManager",
    "EMTranslationResult": "TranslationResult",
    "EMTranslator": "Translator",
    "EMTranslationInfo": "TranslationInfo",
    "EMPresence": "Presence",
    "EMPresenceManager": "PresenceManager",
    "EMPresenceListener": "PresenceListener",
    "EMSilentModeParam": "SilentModeParam",
    "EMSilentModeResult": "SilentModeResult",
    "EMSilentModeTime": "SilentModeTime",
    "EMPushRemindType": "PushRemindType",
    "EMSilentModeParamType": "SilentModeParamType",
    "EMMessageReaction": "MessageReaction",
    "EMMessageReactionChange": "MessageReactionChange",
    "EMChatThreadEvent": "ChatThreadEvent",
    "EMChatThreadManager": "ChatThreadManager",
    "EMChatThreadChangeListener": "ChatThreadChangeListener",
    "EMLogListener": "ChatLogListener",
    "EMStatisticsManager": "ChatStatisticsManager",
    "EMMessageStatistics": "MessageStatistics",
    "EMSearchMessageDirect": "SearchMessageDirect",
    "EMSearchMessageType": "SearchMessageType",
    "EMFetchMessageOption": "FetchMessageOption",
    "EMContact": "Contact",
    "EMConversationFilter": "ConversationFilter",
    "EMMessagePinInfo": "MessagePinInfo",
    "EMRecallMessageInfo": "RecallMessageInfo",
    "EMLoginExtensionInfo": "LoginExtensionInfo",
    "EMCustomConversationFilter": "CustomConversationFilter",
    "EMMessageReactionOperation": "MessageReactionOperation",
    "EMMessageSearchScope": "ChatMessageSearchScope",
    "EMMessage": "ChatMessage",
    "EMChatThread": "ChatThread",
}

# Sort keys by length in descending order to avoid replacement issues
sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
