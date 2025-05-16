import { createContext } from 'react'
// Types
import { ChatContextType, UserContextType } from '../types/Types.ts'

export const UserContext = createContext<UserContextType>({} as UserContextType)

export const ChatContext = createContext<ChatContextType>({} as ChatContextType)
