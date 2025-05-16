import qs from 'qs'
import axios from 'axios'
import { PropsWithChildren, useState, useEffect, useContext } from 'react'
// Types
import {
    UserType,
    LoginRequestType,
    LoginResponseType,
    SignupRequestType,
    SignupResponseType,
    UserMeResponseType,
    ChatType,
    AskAIRequestType,
    AskAIResponseType,
    AdminUploadRequestType,
    AdminUploadResponseType,
    GetNotificationsRequestType,
    GetNotificationsResponseType,
    MarkAsSeenRequestType,
    MarkAsSeenResponseType,
    AdminBroadcastRequestType,
    AdminBroadcastResponseType,
} from '../types/Types.ts'
// Contexts
import { ChatContext, UserContext } from '../contexts/Contexts.ts'

// Server Endpoint
const server = 'http://127.0.0.1:8000'

export const UserProvider = ({ children }: PropsWithChildren) => {
    const [user, setUser] = useState<UserType>(null)
    // Remove Chat History Function
    const { clearChatHistory } = useContext(ChatContext)

    useEffect(() => {
        const token = localStorage.getItem('access_token')

        if (token) {
            fetchUser(token).then()
        }
    }, [])

    const fetchUser = async (token: string) => {
        try {
            const res = await axios.get<UserMeResponseType>(
                `${server}/auth/me`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            )

            setUser(res.data)
        } catch (err) {
            console.error('Failed to fetch user:', err)
        }
    }

    const login = async (data: LoginRequestType) => {
        try {
            const res = await axios.post<LoginResponseType>(
                `${server}/auth/login`,
                qs.stringify(data),
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                }
            )

            const token = res.data.access_token
            localStorage.setItem('access_token', token)
            clearChatHistory()

            await fetchUser(token)
        } catch (err) {
            console.error('Login failed:', err)
            throw err
        }
    }

    const signup = async (data: SignupRequestType) => {
        try {
            await axios.post<SignupResponseType>(
                `${server}/auth/register`,
                data
            )

            const loginData: LoginRequestType = {
                grant_type: 'password',
                username: data.username,
                password: data.password,
                scope: '',
                client_id: 'string',
                client_secret: 'string',
            }

            await login(loginData)
        } catch (err) {
            console.error('Signup failed:', err)
            throw err
        }
    }

    const logout = () => {
        localStorage.removeItem('access_token')
        clearChatHistory()
        setUser(null)
    }

    const uploadFile = async (data: AdminUploadRequestType) => {
        try {
            const token = localStorage.getItem('access_token')

            const res = await axios.post<AdminUploadResponseType>(
                `${server}/admin/upload`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data',
                    },
                }
            )

            return res.data.message
        } catch (err) {
            console.error('File upload failed:', err)
            throw err
        }
    }

    const getNotifications = async (
        params: GetNotificationsRequestType = { fetch_all: false }
    ) => {
        try {
            const token = localStorage.getItem('access_token')

            const res = await axios.get<GetNotificationsResponseType>(
                `${server}/notifications`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                    params,
                }
            )

            return res.data
        } catch (err) {
            console.error('Failed to get notifications:', err)
            throw err
        }
    }

    const markAsSeen = async (data: MarkAsSeenRequestType) => {
        try {
            const token = localStorage.getItem('access_token')

            await axios.post<MarkAsSeenResponseType>(
                `${server}/notifications/mark-as-seen`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            )
        } catch (err) {
            console.error('Failed to mark notifications as seen:', err)
            throw err
        }
    }

    const sendBroadcast = async (data: AdminBroadcastRequestType) => {
        try {
            const token = localStorage.getItem('access_token')

            const res = await axios.post<AdminBroadcastResponseType>(
                `${server}/admin/broadcast`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            )

            return res.data.detail
        } catch (err) {
            console.error('Failed to send broadcast:', err)
            throw err
        }
    }

    return (
        <UserContext.Provider
            value={{
                user,
                login,
                signup,
                logout,
                uploadFile,
                getNotifications,
                markAsSeen,
                sendBroadcast,
            }}
        >
            {children}
        </UserContext.Provider>
    )
}

export const ChatProvider = ({ children }: PropsWithChildren) => {
    const [chatHistory, setChatHistory] = useState<ChatType[]>(() => {
        const stored = sessionStorage.getItem('chat_history')
        return stored ? JSON.parse(stored) : []
    })

    useEffect(() => {
        sessionStorage.setItem('chat_history', JSON.stringify(chatHistory))
    }, [chatHistory])

    const clearChatHistory = () => {
        sessionStorage.removeItem('chat_history')
        setChatHistory([])
    }

    const setTypingFinished = (timestamp: string) => {
        const updatedHistory = chatHistory.map((msg) => {
            if (msg.timestamp === timestamp && msg.sender === 'ai') {
                return { ...msg, messageNotTyped: false }
            }
            return msg
        })

        sessionStorage.setItem('chat_history', JSON.stringify(updatedHistory))

        setChatHistory(updatedHistory)
    }

    const sendMessage = async (data: AskAIRequestType): Promise<ChatType[]> => {
        const userMessage: ChatType = {
            sender: 'user',
            message: data.query,
            timestamp: new Date().toISOString(),
            messageNotTyped: false,
        }

        const updatedHistory = [...chatHistory, userMessage]
        setChatHistory(updatedHistory)

        try {
            const token = localStorage.getItem('access_token')

            const headers = token ? { Authorization: `Bearer ${token}` } : {}

            const res = await axios.post<AskAIResponseType>(
                `${server}/query`,
                data,
                { headers }
            )

            const aiMessage: ChatType = {
                sender: 'ai',
                message: res.data.answer,
                timestamp: new Date().toISOString(),
                messageNotTyped: true,
            }

            const finalHistory = [...updatedHistory, aiMessage]
            setChatHistory(finalHistory)

            return finalHistory
        } catch (err) {
            console.error('Failed to send message:', err)
            throw err
        }
    }

    return (
        <ChatContext.Provider
            value={{
                chatHistory,
                sendMessage,
                clearChatHistory,
                setTypingFinished,
            }}
        >
            {children}
        </ChatContext.Provider>
    )
}
