// Components
import Page from '../components/Page.tsx'
// Functions
import { getFromAssets } from '../functions/Functions.ts'
// Style
import '../styles/pages/AboutPage.css'

const AboutPage = () => {
    return (
        <Page id='about-page'>
            <h1>{'About Us'.toUpperCase()}</h1>
            <div>
                <img
                    src={getFromAssets('img/about-us-image.jpg')}
                    alt='Faculty of Computing and Data Science'
                />
            </div>
            <div className='about-us-content'>
                {/* 1. Meet the Team Behind FCDS Mentor */}
                <section>
                    <h2>Meet the Team Behind FCDS Mentor</h2>
                    <p>
                        FCDS Mentor is the product of a dedicated team of
                        final-year students from the{' '}
                        <strong>
                            Faculty of Computers and Data Science, Alexandria
                            University
                        </strong>
                        . This web application was developed as part of their{' '}
                        <strong>graduation project</strong> to bridge the gap
                        between students and faculty, making essential academic
                        information more accessible.
                    </p>
                </section>
                {/* 2. Our Team */}
                <section>
                    <h2>Our Team</h2>
                    <p>FCDS Mentor was created by:</p>
                    <ul>
                        <li>Asmaa Ibrahim Shabaan</li>
                        <li>Nancy Hamada Mahmoud</li>
                        <li>Fatma Mohamed Abdelsalam</li>
                        <li>Radwa Mohamed Ahmed</li>
                        <li>Mohamed Khaled Mohmed</li>
                        <li>Yomna Rezk Elsayed</li>
                        <li>Youssef Mohamed Farag</li>
                    </ul>
                    <p>
                        Each member of our team has contributed their expertise
                        in data science, web development, and artificial
                        intelligence to create a{' '}
                        <strong>reliable, AI-powered assistant</strong> for FCDS
                        students.
                    </p>
                </section>
                {/* 3. Our Supervisor */}
                <section>
                    <h2>Our Supervisor</h2>
                    <p>
                        We extend our deepest gratitude to{' '}
                        <strong>Dr. Hazem Elfaham</strong>, whose invaluable
                        guidance, expertise, and mentorship played a crucial
                        role in the successful development of FCDS Mentor. His
                        insights and encouragement have been instrumental in
                        shaping our work.
                    </p>
                </section>
                {/* 4. The Vision Behind FCDS Mentor */}
                <section>
                    <h2>The Vision Behind FCDS Mentor</h2>
                    <p>
                        The inspiration for FCDS Mentor came from a simple yet
                        significant challenge —{' '}
                        <strong>
                            students often struggle to find the information they
                            need
                        </strong>{' '}
                        regarding courses, regulations, schedules, and
                        university policies. Our goal was to create an
                        AI-powered system that would:
                    </p>
                    <ul>
                        <li>
                            Provide <strong>instant answers</strong> to academic
                            queries.
                        </li>
                        <li>
                            Improve <strong>communication</strong> between
                            students and faculty.
                        </li>
                        <li>
                            Offer a <strong>centralized knowledge base</strong>{' '}
                            for FCDS-related topics.
                        </li>
                        <li>
                            Make navigation through academic requirements{' '}
                            <strong>seamless and efficient</strong>.
                        </li>
                    </ul>
                    <p>
                        By integrating{' '}
                        <strong>cutting-edge AI technologies</strong>, including{' '}
                        <strong>Retrieval-Augmented Generation (RAG)</strong>,
                        FCDS Mentor ensures accurate, up-to-date responses based
                        on official university data.
                    </p>
                </section>
                {/* 5. About the Faculty of Computers and Data Science (FCDS), Alexandria University */}
                <section>
                    <h2>
                        About the Faculty of Computers and Data Science (FCDS),
                        Alexandria University
                    </h2>
                    <p>
                        The <strong>twenty-first century</strong> is defined by
                        rapid advancements in{' '}
                        <strong>
                            data science, artificial intelligence, and
                            technology
                        </strong>
                        . Recognizing this,{' '}
                        <strong>Alexandria University</strong> established the{' '}
                        <strong>
                            Faculty of Computers and Data Science (FCDS)
                        </strong>{' '}
                        to serve as a leading institution in technological
                        education and research.
                    </p>
                    <p>
                        FCDS was founded to{' '}
                        <strong>
                            equip students with the knowledge and skills
                        </strong>{' '}
                        necessary to navigate the fast-evolving world of data
                        science. The faculty plays a{' '}
                        <strong>
                            crucial role in national and global development
                        </strong>{' '}
                        by:
                    </p>
                    <ul>
                        <li>
                            Preparing graduates to{' '}
                            <strong>analyze, manage, and secure data</strong>{' '}
                            across various industries, from{' '}
                            <strong>healthcare to business and finance</strong>.
                        </li>
                        <li>
                            Advancing research in{' '}
                            <strong>
                                smart systems, cybersecurity, AI, and media
                                technologies
                            </strong>
                            .
                        </li>
                        <li>
                            Providing{' '}
                            <strong>world-class educational programs</strong>{' '}
                            tailored to the demands of today’s job market.
                        </li>
                    </ul>
                    <p>
                        With a <strong>strong commitment to innovation</strong>,
                        FCDS at Alexandria University is dedicated to{' '}
                        <strong>
                            strategic planning and continuous development
                        </strong>
                        . By constantly evolving its programs, the faculty
                        ensures that graduates are well-prepared for{' '}
                        <strong>local and international opportunities</strong>{' '}
                        in the fields of{' '}
                        <strong>computing, AI, and data science</strong>.
                    </p>
                    <p>
                        At <strong>FCDS Mentor</strong>, we are proud to be part
                        of this pioneering institution, contributing to its{' '}
                        <strong>mission of excellence</strong> by making
                        academic knowledge more{' '}
                        <strong>accessible, efficient, and interactive</strong>.
                    </p>
                </section>
            </div>
        </Page>
    )
}

export default AboutPage
