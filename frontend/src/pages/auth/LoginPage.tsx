import { useContext, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
// Components
import Page from '../../components/Page.tsx'
// Contexts
import { UserContext } from '../../contexts/Contexts.ts'
// Functions
import { getFromAssets } from '../../functions/Functions.ts'
// Style
import '../../styles/pages/auth/LoginAndSignupPage.css'

const LoginPage = () => {
    // Login Function
    const { login } = useContext(UserContext)
    // Navigator
    const navigate = useNavigate()
    // Inputs States
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    // Show Password Switch State
    const [showPassword, setShowPassword] = useState(false)

    return (
        <Page id='login-page'>
            <form
                onSubmit={(e) => {
                    e.preventDefault()
                    login({
                        grant_type: 'password',
                        username: username,
                        password: password,
                        scope: '',
                        client_id: 'string',
                        client_secret: 'string',
                    }).then(() => {
                        navigate('/')
                    })
                }}
            >
                <h1>Welcome Back</h1>
                <input
                    type='text'
                    name='username'
                    placeholder='Username'
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <div className='password-container'>
                    <input
                        type={showPassword ? 'text' : 'password'}
                        name='password'
                        placeholder='Password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <img
                        src={getFromAssets(
                            `svg/password_${showPassword ? 'off' : 'on'}.svg`
                        )}
                        alt={`${showPassword ? 'Show' : 'Hide'} Password`}
                        onClick={() => setShowPassword(!showPassword)}
                    />
                </div>
                <button type='submit'>Login</button>
                <div className='links-container'>
                    <Link to='/privacy-policy'>Privacy Policy</Link>
                    <p>|</p>
                    <Link to='/terms-of-use'>Terms Of Use</Link>
                </div>
            </form>
        </Page>
    )
}

export default LoginPage
