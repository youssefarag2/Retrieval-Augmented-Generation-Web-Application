import { useEffect, useState } from 'react'
// Functions
import { detectLanguage, getFromAssets } from '../functions/Functions.ts'
// Types
import { ChatInputProps } from '../types/Types.ts'
// Style
import '../styles/components/ChatInput.css'

const ChatInput = ({ inputState }: ChatInputProps) => {
    // Input Value State
    const [input, setInput] = inputState
    // Language State
    const [language, setLanguage] = useState(detectLanguage('abc'))

    useEffect(() => {
        setLanguage(detectLanguage(input ? input : 'abc'))
    }, [input])

    return (
        <div className='chat-input'>
            <input
                type='text'
                placeholder='Message...'
                value={input}
                onChange={(event) => setInput(event.target.value)}
                lang={language}
                dir={language == 'ar' ? 'rtl' : 'ltr'}
            />
            <button type='submit'>
                <img src={getFromAssets('svg/enter.svg')} alt='Send Message' />
            </button>
        </div>
    )
}

export default ChatInput
