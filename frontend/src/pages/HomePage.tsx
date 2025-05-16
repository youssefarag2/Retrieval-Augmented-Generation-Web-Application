import { Link } from 'react-router-dom'
// Components
import Page from '../components/Page.tsx'
// Functions
import { getFromAssets } from '../functions/Functions.ts'
// Style
import '../styles/pages/HomePage.css'

const HomePage = () => {
    return (
        <Page id='home-page'>
            <div className='left'>
                <h1>Welcome to FCDS Mentor</h1>
                <p className='description'>
                    The FCDS Mentor website is a comprehensive platform designed
                    to support students of the Faculty of Computers and Data
                    Science. This user-friendly website serves as a central hub
                    where students can access all essential information about
                    their college experience
                </p>
                <Link to='chat' className='chat-link'>
                    Chat Now
                </Link>
            </div>
            <div className='right'>
                <div>
                    <img
                        src={getFromAssets('logo/logo.svg')}
                        alt='FCDS Mentor'
                    />
                </div>
            </div>
        </Page>
    )
}

export default HomePage
