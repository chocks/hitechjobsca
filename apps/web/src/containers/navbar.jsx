import React, { Component } from 'react';
import { Link } from 'react-router-dom';


class NavBar extends Component {
    render() {
        const email = 'mailto:hitechjobsca@gmail.com?subject=Hi!';
        let styles = {
            width: '35px',
            height: '35px'
        };

        let phStyles = {
            width: '250px',
            height: '54px'
        };

        let blogToStyles = {
            width: '150px',
            height: '54px',
            marginLeft: '50px'
        };

        return (
            <div className="container-fluid">
                <ul className="nav justify-content-center">
                    <li className="nav-item">
                        <Link className="btn btn-success btn-md" to="/jobs/new">
                            Recruiters - Post Jobs!
                        </Link>
                    </li>
                    <li className="nav-item">
                        <a className="btn btn-md btn-info" href="http://eepurl.com/dAr-5L">Candidates email signup!</a>
                    </li>
                    </ul>
                    <ul className="nav justify-content-center">
                    <li className="nav-item">
                        <a className="btn btn-sm" href="https://www.facebook.com/hitechjobsca/">
                            <img src='/static/f-ogo_RGB_HEX-100.png' style={styles} className="rounded-circle img-thumbnail"></img>
                        </a>
                    </li>
                    <li className="nav-item">
                        <a className="btn btn-sm" href="https://twitter.com/hitechjobsca">
                            <img src='/static/Twitter_Social_Icon_Circle_Color.png' style={styles} className="rounded-circle img-thumbnail"></img>
                        </a>
                    </li>
                    <li className="nav-item">
                        <a className="btn btn-sm" href="https://www.linkedin.com/company/hitechjobsca">
                            <img src='/static/In-2C-101px-R.png' style={styles} className="rounded-circle img-thumbnail"></img>
                        </a>
                    </li>
                    <li className="nav-item">
                        <a className="btn btn-sm" href={email}>
                            <i className="material-icons md-18 rounded-circle img-thumbnail">email</i>
                        </a>
                    </li>
                </ul>
                <ul className="nav justify-content-center">
                    <li className="nav-item">
                    <a href="https://www.producthunt.com/posts/hitechjobsca?utm_source=badge-featured" target="_blank">
                        <img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=142358&theme=light"
                                alt="HiTechJobsCA - Find and promote latest tech jobs in Canada 🇨🇦 | Product Hunt Embed"
                                    style={phStyles} /></a>
                    </li>
                    <li className="nav-item">
                    <a href="https://www.blogto.com/city/2011/01/how_to_search_for_jobs_in_toronto" target="_blank">
                        <img src="/static/logo-blogTO.png"
                                alt="HiTechJobsCA - Find and promote latest tech jobs in Canada 🇨🇦 | As seen on BlogTO"
                                    style={blogToStyles} /></a>
                    </li>
                </ul>
                <br />
            </div>
            );
    }
}

export default NavBar;
