import type { EmitterSubscription, NativeEventEmitter } from 'react-native';

import {
  MTaddChatRoomAdmin,
  MTaddMembersToChatRoomAllowList,
  MTblockChatRoomMembers,
  MTchangeChatRoomDescription,
  MTchangeChatRoomOwner,
  MTchangeChatRoomSubject,
  MTchatRoomChange,
  MTcreateChatRoom,
  MTdestroyChatRoom,
  MTfetchChatRoomAllowListFromServer,
  MTfetchChatRoomAnnouncement,
  MTfetchChatRoomAttributes,
  MTfetchChatRoomBlockList,
  MTfetchChatRoomInfoFromServer,
  MTfetchChatRoomMembers,
  MTfetchChatRoomMuteList,
  MTfetchPublicChatRoomsFromServer,
  MTgetChatRoom,
  MTisMemberInChatRoomAllowListFromServer,
  MTjoinChatRoom,
  MTleaveChatRoom,
  MTmuteAllChatRoomMembers,
  MTmuteChatRoomMembers,
  MTremoveChatRoomAdmin,
  MTremoveChatRoomAttributes,
  MTremoveChatRoomMembers,
  MTremoveMembersFromChatRoomAllowList,
  MTsetChatRoomAttributes,
  MTunBlockChatRoomMembers,
  MTunMuteAllChatRoomMembers,
  MTunMuteChatRoomMembers,
  MTupdateChatRoomAnnouncement,
} from './__internal__/Consts';
import { ExceptionHandler } from './__internal__/ErrorHandler';
import { Native } from './__internal__/Native';
import type { ChatRoomEventListener } from './ChatEvents';
import { chatlog } from './common/ChatConst';
import { ChatCursorResult } from './common/ChatCursorResult';
import { ChatException } from './common/ChatError';
import { ChatPageResult } from './common/ChatPageResult';
import { ChatRoom } from './common/ChatRoom';

/**
 * 聊天室管理类，负责聊天室加入和退出、聊天室列表获取以及成员权限管理等。
 */
export class ChatRoomManager extends Native {
  /**
   * 设置聊天室自定义属性。
   *
   * @param params -
   * - roomId 聊天室 ID。
   * - attributes 要设置的聊天室自定义属性，为键值对（key-value）结构。
   * 在键值对中，key 为属性名，不超过 128 字符；value 为属性值，不超过 4096 字符。
   * 每个聊天室最多有 100 个属性，每个应用的聊天室属性总大小不超过 10 GB。Key 支持以下字符集：
   *   - 26 个小写英文字母 a-z；
   * - 26 个大写英文字母 A-Z；
   * - 10 个数字 0-9；
   * - “_”, “-”, “.”。
   * - deleteWhenLeft: 当前成员退出聊天室是否自动删除该自定义属性。
   *   - (Default)`true`：是
   *   - `false`：否
   * - overwrite: 是否覆盖其他成员设置的属性 key 相同的属性。
   *   - `true`：是
   *   - (Default)`false`：否
   *
   * @returns 若某些属性设置失败，SDK 返回键值对（key-value）结构的属性集合，在每个键值对中 key 为属性 key，value 为失败原因。
   *
   * @throws 如果有异常会在这里抛出，包含错误码和错误描述，详见 {@link ChatError}。
   */
  public async addAttributes(params: {
    roomId: string;
    attributes: { [x: string]: string }[];
    deleteWhenLeft?: boolean;
    overwrite?: boolean;
  }): Promise<Map<string, string>> {
    chatlog.log(`${ChatRoomManager.TAG}: ${this.addAttributes.name}`);
    let r: any = await Native._callMethod(MTsetChatRoomAttributes, {
      [MTsetChatRoomAttributes]: {
        roomId: params.roomId,
        attributes: params.attributes,
        autoDelete: params.deleteWhenLeft ?? false,
        forced: params.overwrite ?? false,
      },
    });
    ChatRoomManager.checkErrorFromResult(r);
    const ret: Map<string, string> = new Map();
    if (r?.[MTsetChatRoomAttributes]) {
      Object.entries(r?.[MTsetChatRoomAttributes]).forEach(
        (v: [string, any]) => {
          ret.set(v[0], v[1]);
        }
      );
    }
    return ret;
  }

    /**
   * 设置聊天室自定义属性。
   *
   * @param params -
   * - roomId 聊天室 ID。
   * - attributes 要设置的聊天室自定义属性，为键值对（key-value）结构。
   * 在键值对中，key 为属性名，不超过 128 字符；value 为属性值，不超过 4096 字符。
   * 每个聊天室最多有 100 个属性，每个应用的聊天室属性总大小不超过 10 GB。Key 支持以下字符集：
   *   - 26 个小写英文字母 a-z；
   * - 26 个大写英文字母 A-Z；
   * - 10 个数字 0-9；
   * - “_”, “-”, “.”。
   * - deleteWhenLeft: 当前成员退出聊天室是否自动删除该自定义属性。
   *   - (Default)`true`：是
   *   - `false`：否
   * - overwrite: 是否覆盖其他成员设置的属性 key 相同的属性。
   *   - `true`：是
   *   - (Default)`false`：否
   *
   * @returns 若某些属性设置失败，SDK 返回键值对（key-value）结构的属性集合，在每个键值对中 key 为属性 key，value 为失败原因。
   *
   * @throws 如果有异常会在这里抛出，包含错误码和错误描述，详见 {@link ChatError}。
   */
  public async addAttributes2(params: {
    roomId: string;
    attributes: { [x: string]: string }[];
    deleteWhenLeft?: boolean;
    overwrite?: boolean;
  }): Promise<Map<string, string>> {
    chatlog.log(`${ChatRoomManager.TAG}: ${this.addAttributes.name}`);
    let r: any = await Native._callMethod(MTsetChatRoomAttributes, {
      [MTsetChatRoomAttributes]: {
        roomId: params.roomId,
        attributes: params.attributes,
        autoDelete: params.deleteWhenLeft ?? false,
        forced: params.overwrite ?? false,
      },
    });
    ChatRoomManager.checkErrorFromResult(r);
    const ret: Map<string, string> = new Map();
    if (r?.[MTsetChatRoomAttributes]) {
      Object.entries(r?.[MTsetChatRoomAttributes]).forEach(
        (v: [string, any]) => {
          ret.set(v[0], v[1]);
        }
      );
    }
    return ret;
  }
}
