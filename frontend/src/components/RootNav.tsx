import { useContext, useEffect, useState } from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
// Components
import Container from './Container.tsx'
import NotificationMessage from './NotificationMessage.tsx'
// Contexts
import { UserContext } from '../contexts/Contexts.ts'
// Types
import { NotificationType } from '../types/Types.ts'
// Functions
import { capitalize, getFromAssets } from '../functions/Functions.ts'
// Style
import '../styles/components/RootNav.css'

const RootNav = () => {
    // User Object & Logout Function
    const { user, logout, getNotifications, markAsSeen } =
        useContext(UserContext)
    // Navigator
    const navigate = useNavigate()
    // Dropdown Opened State
    const [dropdownOpen, setDropdownOpen] = useState(false)
    // Notifications Dropdown State
    const [notificationsOpen, setNotificationsOpen] = useState(false)
    // Notifications State
    const [notifications, setNotifications] = useState<NotificationType[]>([])

    useEffect(() => {
        getNotifications().then((res) => setNotifications(res))
    }, [])

    return (
        <nav id='root-nav'>
            <Container>
                <div className='left'>
                    <Link
                        to='/'
                        onClick={() => {
                            setDropdownOpen(false)
                        }}
                    >
                        <img
                            src={getFromAssets('logo/logo.svg')}
                            alt='FCDS Mentor'
                        />
                    </Link>
                </div>
                <div className='right'>
                    {user && (
                        <>
                            <div className='notifications-container'>
                                <button
                                    className='open-notifications'
                                    onClick={() =>
                                        setNotificationsOpen(!notificationsOpen)
                                    }
                                >
                                    <img
                                        src={getFromAssets(
                                            `svg/notifications.svg`
                                        )}
                                        alt='Open Notifications'
                                    />
                                    {notifications.length > 0 && (
                                        <p>{notifications.length}</p>
                                    )}
                                </button>
                                <div
                                    className='notifications-dropdown'
                                    style={{
                                        visibility: notificationsOpen
                                            ? 'visible'
                                            : 'hidden',
                                    }}
                                >
                                    {notifications.length > 0 ? (
                                        notifications.map((notification) => (
                                            <NotificationMessage
                                                key={
                                                    'notification' +
                                                    notification.id
                                                }
                                                notification={notification}
                                                onClick={async () => {
                                                    try {
                                                        await markAsSeen({
                                                            notification_ids: [
                                                                notification.id,
                                                            ],
                                                        })
                                                        setNotifications(
                                                            (prev) =>
                                                                prev.filter(
                                                                    (n) =>
                                                                        n.id !==
                                                                        notification.id
                                                                )
                                                        )
                                                    } catch (err) {
                                                        console.error(
                                                            'Failed to mark as seen:',
                                                            err
                                                        )
                                                    }
                                                }}
                                            />
                                        ))
                                    ) : (
                                        <p className='empty'>
                                            No new notifications
                                        </p>
                                    )}
                                </div>
                            </div>
                            <div className='logged-in'>
                                <h1>{user.username}</h1>
                                <h2>{capitalize(user.role)}</h2>
                                {user.level && <h2>{`Level ${user.level}`}</h2>}
                                <button
                                    onClick={() => {
                                        logout()
                                        navigate('/')
                                    }}
                                >
                                    Logout
                                </button>
                            </div>
                        </>
                    )}
                    <button
                        className='open-dropdown'
                        onClick={() => {
                            setDropdownOpen(!dropdownOpen)
                        }}
                    >
                        <p>PAGES</p>
                        <img
                            src={getFromAssets(
                                `svg/${dropdownOpen ? 'close_dropdown' : 'dropdown'}.svg`
                            )}
                            alt='Dropdown'
                        />
                    </button>
                    <div
                        className='dropdown'
                        style={{
                            visibility: dropdownOpen ? 'visible' : 'hidden',
                        }}
                    >
                        <NavLink
                            to='/'
                            onClick={() => {
                                setDropdownOpen(!dropdownOpen)
                            }}
                        >
                            Home
                        </NavLink>
                        <NavLink
                            to='/chat'
                            onClick={() => {
                                setDropdownOpen(!dropdownOpen)
                            }}
                        >
                            Chat
                        </NavLink>
                        <NavLink
                            to='/about'
                            onClick={() => {
                                setDropdownOpen(!dropdownOpen)
                            }}
                        >
                            About
                        </NavLink>
                        {user?.role === 'admin' && (
                            <NavLink
                                to='/upload'
                                onClick={() => {
                                    setDropdownOpen(!dropdownOpen)
                                }}
                            >
                                Upload
                            </NavLink>
                        )}
                        {user?.role === 'admin' && (
                            <NavLink
                                to='/broadcast'
                                onClick={() => {
                                    setDropdownOpen(!dropdownOpen)
                                }}
                            >
                                Broadcast
                            </NavLink>
                        )}
                        {!user && (
                            <>
                                <Link
                                    to='/auth/login'
                                    onClick={() => {
                                        setDropdownOpen(!dropdownOpen)
                                    }}
                                >
                                    Login
                                </Link>
                                <Link
                                    to='/auth/signup'
                                    onClick={() => {
                                        setDropdownOpen(!dropdownOpen)
                                    }}
                                >
                                    Signup
                                </Link>
                            </>
                        )}
                    </div>
                </div>
            </Container>
        </nav>
    )
}
export default RootNav
