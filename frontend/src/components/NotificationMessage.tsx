import moment from 'moment'
// Functions
import { getFromAssets } from '../functions/Functions.ts'
// Types
import { NotificationMessageProps } from '../types/Types.ts'
// Style
import '../styles/components/NotificationMessage.css'

const NotificationMessage = ({
    notification,
    onClick,
}: NotificationMessageProps) => {
    return (
        <div className='notification-message'>
            <div className='info'>
                <h1>
                    Notification • {moment(notification.timestamp).fromNow()}
                </h1>
                <p>{notification.message}</p>
            </div>
            <button onClick={onClick}>
                <img src={getFromAssets('svg/seen.svg')} alt='Mark As Read' />
            </button>
        </div>
    )
}

export default NotificationMessage
