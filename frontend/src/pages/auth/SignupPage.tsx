import { useContext, useState, FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { AxiosError } from 'axios'
// Components
import Page from '../../components/Page.tsx'
// Contexts
import { UserContext } from '../../contexts/Contexts.ts'
// Functions
import { getFromAssets } from '../../functions/Functions.ts'
// Types
import { ErrorMessageType, ValidationErrorDetail } from '../../types/Types.ts'
// Style
import '../../styles/pages/auth/LoginAndSignupPage.css'

const SignupPage = () => {
    // Signup Function
    const { signup } = useContext(UserContext)
    // Navigator
    const navigate = useNavigate()
    // Inputs States
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [level, setLevel] = useState('1')
    // Show Password Switch State
    const [showPassword, setShowPassword] = useState(false)
    // If there is an error returned from backend State
    const [error, setError] = useState<ErrorMessageType>({})

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault()
        setError({})

        try {
            await signup({
                username,
                password,
                role: 'student',
                level: parseInt(level),
            })
            navigate('/')
        } catch (err) {
            const axiosError = err as AxiosError<{
                detail: ValidationErrorDetail[]
            }>
            const detail = axiosError.response?.data?.detail
            const fieldErrors: ErrorMessageType = {}

            if (Array.isArray(detail)) {
                detail.forEach((issue) => {
                    const field = issue?.loc?.[1]
                    if (field === 'username') {
                        fieldErrors.username = issue.msg
                    } else if (field === 'password') {
                        fieldErrors.password = issue.msg
                    } else {
                        fieldErrors.general = issue.msg
                    }
                })
            } else {
                fieldErrors.general =
                    (axiosError.response?.data?.detail as unknown as string) ||
                    axiosError.message ||
                    'Signup failed'
            }

            setError(fieldErrors)
        }
    }

    return (
        <Page id='signup-page'>
            <form onSubmit={handleSubmit}>
                <h1>Create Account</h1>
                <input
                    type='text'
                    name='username'
                    placeholder='Username'
                    value={username}
                    onChange={(e) => {
                        setUsername(e.target.value)
                        if (error.username || error.general)
                            setError((prev) => ({
                                ...prev,
                                general: undefined,
                                username: undefined,
                            }))
                    }}
                    className={
                        error.username || error.general ? 'input-error' : ''
                    }
                />
                {error.username && (
                    <p className='error-message'>{error.username}</p>
                )}
                <div className='password-container'>
                    <input
                        type={showPassword ? 'text' : 'password'}
                        name='password'
                        placeholder='Password'
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value)
                            if (error.password || error.general)
                                setError((prev) => ({
                                    ...prev,
                                    general: undefined,
                                    password: undefined,
                                }))
                        }}
                        className={
                            error.password || error.general ? 'input-error' : ''
                        }
                    />
                    <img
                        src={getFromAssets(
                            `svg/password_${showPassword ? 'off' : 'on'}.svg`
                        )}
                        alt={`${showPassword ? 'Show' : 'Hide'} Password`}
                        onClick={() => setShowPassword(!showPassword)}
                    />
                </div>
                {error.password && (
                    <p className='error-message'>{error.password}</p>
                )}

                <div className='levels-container'>
                    {[1, 2, 3, 4].map((lvl) => (
                        <label key={lvl}>
                            Level {lvl}
                            <input
                                type='radio'
                                name='level'
                                value={lvl}
                                checked={level === lvl.toString()}
                                onChange={(e) => setLevel(e.target.value)}
                            />
                        </label>
                    ))}
                </div>

                {error.general && (
                    <p className='error-message'>{error.general}</p>
                )}

                <button type='submit'>Create Account</button>
                <div className='links-container'>
                    <Link to='/privacy-policy'>Privacy Policy</Link>
                    <p>|</p>
                    <Link to='/terms-of-use'>Terms Of Use</Link>
                </div>
            </form>
        </Page>
    )
}

export default SignupPage
