import { useContext, useState, useRef, useEffect } from 'react'
// Components
import Page from '../../components/Page.tsx'
import ChatInput from '../../components/ChatInput.tsx'
import ChatMessage from '../../components/ChatMessage.tsx'
import MessageLoading from '../../components/MessageLoading.tsx'
// Contexts
import { ChatContext, UserContext } from '../../contexts/Contexts.ts'
// Style
import '../../styles/pages/chat/ChatPage.css'

const ChatPage = () => {
    // User Object
    const { user } = useContext(UserContext)
    // Chat History & Send Message Function
    const { chatHistory, sendMessage } = useContext(ChatContext)
    // User Message
    const [userMessage, setUserMessage] = useState<string>('')
    // Reference to scroll to the end of chat
    const messagesEndRef = useRef<HTMLDivElement | null>(null)

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
        }
    }, [chatHistory])

    return (
        <Page id='chat-page'>
            <>
                {chatHistory.length > 0 ? (
                    <div className='chat-with-history'>
                        {chatHistory.map((messageInChat, index) => (
                            <ChatMessage
                                message={messageInChat}
                                username={user ? user.username : 'Guest'}
                                key={index}
                            />
                        ))}
                        {chatHistory[chatHistory.length - 1].sender ===
                            'user' && <MessageLoading />}
                        <div ref={messagesEndRef}></div>
                    </div>
                ) : (
                    <div className='first-message'>
                        <h1>What's on your mind?</h1>
                    </div>
                )}
                <form
                    onSubmit={(e) => {
                        e.preventDefault()
                        setUserMessage('')
                        sendMessage({ query: userMessage }).then()
                    }}
                    className={
                        chatHistory.length == 0
                            ? 'first-message'
                            : 'chat-with-history'
                    }
                >
                    <ChatInput inputState={[userMessage, setUserMessage]} />
                </form>
            </>
        </Page>
    )
}

export default ChatPage
