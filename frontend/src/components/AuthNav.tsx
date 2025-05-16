import { Link } from 'react-router-dom'
// Components
import Container from './Container.tsx'
// Functions
import { getFromAssets } from '../functions/Functions.ts'
// Style
import '../styles/components/AuthNav.css'

const AuthNav = () => {
    return (
        <nav id='auth-nav'>
            <Container>
                <div>
                    <Link to='/'>
                        <img
                            src={getFromAssets('logo/logo.svg')}
                            alt='FCDS Mentor'
                        />
                    </Link>
                </div>
            </Container>
        </nav>
    )
}

export default AuthNav
