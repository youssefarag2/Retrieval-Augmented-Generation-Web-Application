import { useContext } from 'react'
import { Link } from 'react-router-dom'
// Components
import Container from './Container.tsx'
// Contexts
import { UserContext } from '../contexts/Contexts.ts'
// Functions
import { getFromAssets } from '../functions/Functions.ts'
// Style
import '../styles/components/Footer.css'

const Footer = () => {
    // User Object
    const { user } = useContext(UserContext)

    return (
        <footer>
            <Container>
                <div className='top'>
                    <div className='left'>
                        <div>
                            <img
                                src={getFromAssets('logo/logo.svg')}
                                alt='FCDS Mentor'
                            />
                        </div>
                    </div>
                    <div className='right'>
                        <h1>{'Navigation'.toUpperCase()}</h1>
                        <div>
                            <Link to='/'>
                                <img
                                    src={getFromAssets('svg/footer_arrow.svg')}
                                    alt='Arrow'
                                />
                                Home
                            </Link>
                            <Link to='/chat'>
                                <img
                                    src={getFromAssets('svg/footer_arrow.svg')}
                                    alt='Arrow'
                                />
                                Chat
                            </Link>
                            <Link to='/about'>
                                <img
                                    src={getFromAssets('svg/footer_arrow.svg')}
                                    alt='Arrow'
                                />
                                About
                            </Link>
                            {user?.role === 'admin' && (
                                <Link to='/upload'>
                                    <img
                                        src={getFromAssets(
                                            'svg/footer_arrow.svg'
                                        )}
                                        alt='Arrow'
                                    />
                                    Upload
                                </Link>
                            )}
                            {!user && (
                                <>
                                    <Link to='/auth/login'>
                                        <img
                                            src={getFromAssets(
                                                'svg/footer_arrow.svg'
                                            )}
                                            alt='Arrow'
                                        />
                                        Login
                                    </Link>
                                    <Link to='/auth/signup'>
                                        <img
                                            src={getFromAssets(
                                                'svg/footer_arrow.svg'
                                            )}
                                            alt='Arrow'
                                        />
                                        Signup
                                    </Link>
                                </>
                            )}
                        </div>
                    </div>
                </div>
                <div className='bottom'>
                    <div className='left'>
                        <p>All Rights Reserved - FCDS Mentor</p>
                    </div>
                    <div className='right'>
                        <Link to='/privacy-policy'>Privacy Policy</Link>
                        <p>|</p>
                        <Link to='/terms-of-use'>Terms Of Use</Link>
                    </div>
                </div>
            </Container>
        </footer>
    )
}

export default Footer
