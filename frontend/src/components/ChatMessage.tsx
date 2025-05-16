import ReactMarkdown from 'react-markdown'
import { useContext, useEffect, useState } from 'react'
// Context
import { ChatContext } from '../contexts/Contexts.ts'
// Functions
import { capitalize, detectLanguage } from '../functions/Functions.ts'
// Types
import { ChatMessageProps } from '../types/Types.ts'
// Style
import '../styles/components/ChatMessage.css'

const ChatMessage = ({ message, username }: ChatMessageProps) => {
    const isUser = message.sender === 'user'
    // Chat History Setter
    const { setTypingFinished } = useContext(ChatContext)
    // Writing Effect State
    const [displayedMessage, setDisplayedMessage] = useState(
        isUser ? message.message : ''
    )
    // Blinking Cursor State
    const [isTyping, setIsTyping] = useState(!isUser)
    // Language State
    const [language, _] = useState(detectLanguage(message.message))

    useEffect(() => {
        if (!isUser && message.messageNotTyped) {
            let index = 0

            const typeNextChar = () => {
                const char = message.message.charAt(index)
                setDisplayedMessage((prev) => prev + char)
                index++

                if (index >= message.message.length) {
                    setIsTyping(false)
                    setTypingFinished(message.timestamp)
                    return
                }

                // Human-like variable delay
                let baseDelay = 10

                // Add randomness (±10ms)
                const delay = baseDelay + Math.floor(Math.random() * 10)
                setTimeout(typeNextChar, delay)
            }

            typeNextChar()
        }
    }, [message.message, isUser])

    return (
        <div className={`chat-message-${message.sender}`}>
            <div className='sender'>
                {isUser ? capitalize(username) : 'FCDS Mentor'}
            </div>
            <div
                className='message'
                lang={language}
                dir={language == 'ar' ? 'rtl' : 'ltr'}
            >
                {
                    <ReactMarkdown>
                        {message.messageNotTyped
                            ? displayedMessage
                            : message.message}
                    </ReactMarkdown>
                }
                {isTyping && message.messageNotTyped && (
                    <span className='blinking-cursor'>_</span>
                )}
            </div>
            <div className='timestamp'>
                {new Date(message.timestamp).toLocaleTimeString('en-US', {
                    hour: 'numeric',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: true,
                })}
            </div>
        </div>
    )
}

export default ChatMessage
