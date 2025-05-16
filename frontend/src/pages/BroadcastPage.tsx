import { useContext, useState, useEffect, FormEvent } from 'react'
// Components
import Page from '../components/Page.tsx'
// Contexts
import { UserContext } from '../contexts/Contexts.ts'
// Style
import '../styles/pages/UploadAndBroadcastPages.css'

const BroadcastPage = () => {
    // User Object & Upload File Function (IF ADMIN)
    const { user, sendBroadcast } = useContext(UserContext)
    // Message State
    const [message, setMessage] = useState('')
    // Broadcast Message State
    const [broadcastMessage, setBroadcastMessage] = useState('')
    // Target Level State
    const [targetLevel, setTargetLevel] = useState('0')
    // Loading State
    const [loading, setLoading] = useState(false)
    // Loading State
    const [dots, setDots] = useState('')

    useEffect(() => {
        if (loading) {
            const interval = setInterval(() => {
                setDots((prev) => (prev.length < 3 ? prev + '.' : ''))
            }, 500)
            return () => clearInterval(interval)
        }
    }, [loading])

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault()

        if (!broadcastMessage.trim()) {
            setMessage('Message cannot be empty.')
            return
        }

        setLoading(true)

        try {
            const res = await sendBroadcast({
                message: broadcastMessage,
                target_level:
                    targetLevel === '0' ? 'all' : parseInt(targetLevel),
            })

            setMessage(res)
            setBroadcastMessage('')
            setTargetLevel('0')
        } catch {
            setMessage('Something went wrong.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <Page id='upload-page'>
            {loading ? (
                <h1 className='sending-effect'>Sending{dots}</h1>
            ) : (
                <>
                    <h1>Send Broadcast</h1>
                    {user?.role === 'admin' ? (
                        <>
                            <p>{message}</p>
                            <form onSubmit={handleSubmit}>
                                <textarea
                                    value={broadcastMessage}
                                    placeholder='Write your message here...'
                                    name='broadcast_message'
                                    onChange={(e) =>
                                        setBroadcastMessage(e.target.value)
                                    }
                                ></textarea>

                                <h2>Send Message to</h2>
                                <div className='levels-container'>
                                    {[0, 1, 2, 3, 4].map((lvl) => (
                                        <label key={lvl}>
                                            {lvl === 0 ? 'All' : `Level ${lvl}`}
                                            <input
                                                type='radio'
                                                name='target_level'
                                                value={lvl}
                                                checked={
                                                    targetLevel ===
                                                    lvl.toString()
                                                }
                                                onChange={(e) =>
                                                    setTargetLevel(
                                                        e.target.value
                                                    )
                                                }
                                            />
                                        </label>
                                    ))}
                                </div>

                                <button type='submit'>Send</button>
                            </form>
                        </>
                    ) : (
                        <p>You are unauthorized to send broadcasts.</p>
                    )}
                </>
            )}
        </Page>
    )
}

export default BroadcastPage
