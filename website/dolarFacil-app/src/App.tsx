import axios from 'axios';
import React from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import DatePicker from './components/DatePicker';
import Top from './components/Top';

class App extends React.Component{
  state = { details: [], }

  componentDidMount(){
      let data;
      axios.get('http://localhost:8000/')
      .then(res=>{
        data = res.data;
        this.setState({
          details: res.data
        });
      })
      .catch((err) => { 
        console.error('Error fetching data:', err)
      })
  }

  render(){
    return(
      <>
      <Top/>
      <div>
        <>
          <DatePicker/>
        </>
        {this.state.details.map((output,index)=> (
          <div key={index}>
            <h1>{output.DataSocilitada}</h1>
          </div>
        ))}
      </div>
    </>
    )
  }
}

export default App;
