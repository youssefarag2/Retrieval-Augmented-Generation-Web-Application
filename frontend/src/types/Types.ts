import { Dispatch, SetStateAction, PropsWithChildren } from 'react'

// Props
export type PageProps = PropsWithChildren & {
    id?: string
}

export type ChatInputProps = {
    inputState: [string, Dispatch<SetStateAction<string>>]
}

export type ChatMessageProps = {
    message: ChatType
    username: string
}

export type NotificationMessageProps = {
    notification: NotificationType
    onClick: () => void
}

// Objects
export type ChatType = {
    sender: 'user' | 'ai'
    message: string
    timestamp: string
    messageNotTyped: boolean
}

export type UserType = {
    id: number
    username: string
    role: 'student' | 'admin'
    level: number | null
} | null

export type ErrorMessageType = {
    username?: string
    password?: string
    general?: string
}

export type ValidationErrorDetail = {
    loc: [string, string]
    msg: string
    type: string
}

export type DocumentAccessLevelType =
    | 'public'
    | 'all_students'
    | 'level_1'
    | 'level_2'
    | 'level_3'
    | 'level_4'
    | 'admin_only'

export type NotificationType = {
    id: number
    message: string
    target_level: 'all' | number | null
    document_internal_id: string | null
    timestamp: string
    is_seen: boolean
}

// Contexts
export type ChatContextType = {
    chatHistory: ChatType[] | []
    sendMessage: (data: AskAIRequestType) => Promise<ChatType[]>
    clearChatHistory: () => void
    setTypingFinished: (timestamp: string) => void
}

export type UserContextType = {
    user: UserType
    uploadFile: (data: AdminUploadRequestType) => Promise<string>
    login: (data: LoginRequestType) => Promise<void>
    signup: (data: SignupRequestType) => Promise<void>
    getNotifications: (
        params?: GetNotificationsRequestType
    ) => Promise<GetNotificationsResponseType>
    markAsSeen: (data: MarkAsSeenRequestType) => Promise<void>
    sendBroadcast: (data: AdminBroadcastRequestType) => Promise<string>
    logout: () => void
}

// Backend
/* ------- ENDPOINT: POST /auth/register ------- */
export type SignupRequestType = {
    username: string
    password: string
    role: 'student'
    level: number | null
}

export type SignupResponseType = UserType & {}

/* ------- ENDPOINT: POST /auth/login ------- */
export type LoginRequestType = {
    grant_type: string
    username: string
    password: string
    scope: string
    client_id: string
    client_secret: string
}

export type LoginResponseType = {
    access_token: string
    token_type: string
}

/* ------- ENDPOINT: GET /auth/user/me ------- */
export type UserMeResponseType = UserType & {}

/* ------- ENDPOINT: POST /admin/upload ------- */
export type AdminUploadRequestType = {
    file: File
    notification_message: string | null
    notification_target_level: 'all' | number | null
    doc_access_target: DocumentAccessLevelType
}

export type AdminUploadResponseType = {
    filename: string
    message: string
    doc_internal_id: string
    error: string | null
    notification_sent: boolean
}

/* ------- ENDPOINT: POST /admin/broadcast ------- */
export type AdminBroadcastRequestType = {
    message: string
    target_level: 'all' | number | null
}

export type AdminBroadcastResponseType = {
    detail: string
}

/* ------- ENDPOINT: POST /query/ask ------- */
export type AskAIRequestType = {
    query: string
}

export type AskAIResponseType = {
    answer: string
    sources: object[]
}

/* ------- ENDPOINT: GET /notifications ------- */
export type GetNotificationsRequestType = {
    fetch_all: boolean
}

export type GetNotificationsResponseType = NotificationType[]

/* ------- ENDPOINT: GET /notifications/mark-as-seen ------- */
export type MarkAsSeenRequestType = {
    notification_ids: number[]
}

export type MarkAsSeenResponseType = {}
