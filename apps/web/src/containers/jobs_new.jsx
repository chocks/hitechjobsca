import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import NavBar from './navbar';
import Header from './header';


class JobsNew extends Component {
    render() {
        const email = 'mailto:hitechjobsca@gmail.com?subject=reg: Promoted Listings';
        return (
            <div className="row">
                <Header />
                <NavBar />
                <div className="container-fluid">
                    <div className="card text-center">
                    <div className="card-body">
                        <h5 className="card-title">Promoted Listings! Just CAD $249 for 60 days</h5>
                        <p className="card-text">
                        Try our unique 🦄 digital marketing technique for your 💼 job listings. Get higher number of applicants for your posting 📈 and fill faster!<br />
                        We promote listings on several social media channels such as Twitter, LinkedIn, Facebook etc. <br />
                        Listings are also included in the bi-weekly ✉️ email newsletters to our subscriber base.
                        </p>
                         <a className="btn btn-primary" href={email}>Get in touch - Email</a>
                    </div>
                    </div>
                </div>
            </div>
        );
    }
}


export default JobsNew;
