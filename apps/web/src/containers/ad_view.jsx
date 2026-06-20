import React, { Component } from 'react';



class AdView extends Component {
    render() {
        let styles = {
            height: '144px',
            width: '320px'
        };
        return (
            <div className="embed-responsive embed-responsive-1by1 col-sm-8 offset-md-4" style={styles}>
                <iframe className="embed-responsive-item align-self-center" src="https://makerads.xyz/ad"></iframe>
            </div>
        );
    }
}

export default AdView;
