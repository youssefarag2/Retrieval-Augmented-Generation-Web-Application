import {
    useContext,
    useState,
    useCallback,
    useRef,
    DragEvent,
    useEffect,
} from 'react'
// Components
import Page from '../components/Page.tsx'
// Contexts
import { UserContext } from '../contexts/Contexts.ts'
// Functions
import {
    capitalize,
    detectLanguage,
    getFromAssets,
} from '../functions/Functions.ts'
// Types
import { DocumentAccessLevelType } from '../types/Types.ts'
// Style
import '../styles/pages/UploadAndBroadcastPages.css'

const UploadPage = () => {
    // User Object & Upload File Function (IF ADMIN)
    const { user, uploadFile } = useContext(UserContext)
    // File State
    const [file, setFile] = useState<File | null>(null)
    // File Input Reference
    const fileInputRef = useRef<HTMLInputElement>(null)
    // Message
    const [message, setMessage] = useState<string>('')
    // Loading State
    const [loading, setLoading] = useState(false)
    // Drag & Drop Boolean
    const [isDragging, setIsDragging] = useState(false)
    // Language State
    const [language, setLanguage] = useState(detectLanguage('abc'))
    // Uploading Animation Dots
    const [dots, setDots] = useState('')
    // Broadcast Message State
    const [broadcastMessage, setBroadcastMessage] = useState('')
    // Notification Target Level State
    const [notificationTargetLevel, setNotificationTargetLevel] = useState('0')
    // Document Access Level State
    const [docAccessLevel, setDocAccessLevel] =
        useState<DocumentAccessLevelType>('public')

    const handleDrop = useCallback((e: DragEvent<HTMLDivElement>) => {
        e.preventDefault()
        setIsDragging(false)
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            setFile(e.dataTransfer.files[0])
        }
    }, [])

    useEffect(() => {
        setLanguage(detectLanguage(file?.name ? file.name : 'abc'))
    }, [file?.name])

    useEffect(() => {
        if (loading) {
            const interval = setInterval(() => {
                setDots((prev) => (prev.length < 3 ? prev + '.' : ''))
            }, 500)
            return () => clearInterval(interval)
        }
    }, [loading])

    return (
        <Page id='upload-page'>
            {loading ? (
                <h1 className='embedding-effect'>Embedding{dots}</h1>
            ) : (
                <>
                    <h1>Upload File</h1>
                    {user?.role === 'admin' ? (
                        <>
                            <p>{message}</p>
                            <form
                                onSubmit={(e) => {
                                    e.preventDefault()
                                    if (file) {
                                        setLoading(true)
                                        uploadFile({
                                            file: file,
                                            notification_message:
                                                broadcastMessage,
                                            notification_target_level: parseInt(
                                                notificationTargetLevel
                                            ),
                                            doc_access_target: docAccessLevel,
                                        })
                                            .then((res) => {
                                                setMessage(res)
                                                setFile(null)
                                                setBroadcastMessage('')
                                                setNotificationTargetLevel('0')
                                                setDocAccessLevel('public')
                                                setLoading(false)
                                            })
                                            .catch(() => {
                                                setMessage(
                                                    'Something went wrong.'
                                                )
                                                setLoading(false)
                                            })
                                    }
                                }}
                            >
                                <div
                                    className='drag-and-drop-area'
                                    onClick={() =>
                                        fileInputRef.current?.click()
                                    }
                                    onDrop={handleDrop}
                                    onDragOver={(
                                        e: DragEvent<HTMLDivElement>
                                    ) => {
                                        e.preventDefault()
                                        setIsDragging(true)
                                    }}
                                    onDragLeave={() => setIsDragging(false)}
                                >
                                    {file && (
                                        <img
                                            src={getFromAssets(
                                                `svg/${
                                                    file?.type ===
                                                    'application/pdf'
                                                        ? 'file-pdf.svg'
                                                        : file?.type ===
                                                            'text/plain'
                                                          ? 'file-txt.svg'
                                                          : 'file-docx.svg'
                                                }`
                                            )}
                                            alt='File Icon'
                                        />
                                    )}
                                    <p
                                        lang={language}
                                        dir={language == 'ar' ? 'rtl' : 'ltr'}
                                    >
                                        {isDragging
                                            ? 'Drop the file here!'
                                            : file
                                              ? file.name
                                              : 'Drag & drop or click to select a file'}
                                    </p>
                                    <input
                                        type='file'
                                        name='file'
                                        ref={fileInputRef}
                                        onChange={(e) => {
                                            if (
                                                e.target.files &&
                                                e.target.files.length > 0
                                            ) {
                                                setFile(e.target.files[0])
                                            }
                                        }}
                                    />
                                </div>
                                <h2>Broadcast Message</h2>
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
                                                    notificationTargetLevel ===
                                                    lvl.toString()
                                                }
                                                onChange={(e) =>
                                                    setNotificationTargetLevel(
                                                        e.target.value
                                                    )
                                                }
                                            />
                                        </label>
                                    ))}
                                </div>
                                <h2>Document Accessed by</h2>
                                <div className='levels-container'>
                                    {[
                                        'public',
                                        'all_students',
                                        'level_1',
                                        'level_2',
                                        'level_3',
                                        'level_4',
                                        'admin_only',
                                    ].map((lvl) => (
                                        <label key={lvl}>
                                            {lvl
                                                .split('_')
                                                .map((text) => capitalize(text))
                                                .join(' ')}
                                            <input
                                                type='radio'
                                                name='doc_access_level'
                                                value={lvl}
                                                checked={
                                                    docAccessLevel ===
                                                    lvl.toString()
                                                }
                                                onChange={(e) =>
                                                    setDocAccessLevel(
                                                        e.target
                                                            .value as DocumentAccessLevelType
                                                    )
                                                }
                                            />
                                        </label>
                                    ))}
                                </div>
                                <button type='submit'>Upload</button>
                            </form>
                        </>
                    ) : (
                        <>
                            <p>You are unauthorized to upload files.</p>
                        </>
                    )}
                </>
            )}
        </Page>
    )
}

export default UploadPage
