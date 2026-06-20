import React, { Component } from 'react';

class Header extends Component {
    render() {
        let styles = {
            display: 'block',
            marginLeft: 'auto',
            marginRight: 'auto',
            width: '50%'
          };

        return (
            <div className="card bg-light mb-3 float-center">
                <a href="/">
                    <img className="card-img-top" style={styles} src="/static/color_logo_transparent.svg" alt="HiTechJobsCA" />
                </a>
            </div>
        );
    }
}

export default Header;