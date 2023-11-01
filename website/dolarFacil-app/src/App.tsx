import axios from 'axios';
import "bootstrap/dist/css/bootstrap.min.css";
import Top from './components/Top';
import Footer from './components/Footer'
import React from 'react';

class App extends React.Component{
  constructor(){
    super();
    this.state={
        DataSolicitada: '',
    }
    this.changeHandler=this.changeHandler.bind(this);
    this.submitForm=this.submitForm.bind(this);
  }
  changeHandler(event) {
    this.setState({
      DataSolicitada: event.target.value
    });
    console.log(this.state);
  }

  submitForm(event) {
    event.preventDefault();
    axios.post(`http://localhost:8000/cotacao/${this.state.DataSolicitada}/`)
    .then((response) => {
      console.log("Cotação armazenada com sucesso",response)
    })
    .catch((error) => {
      console.error('Erro ao armazenar cotação:', error);
    })
    console.log(this.state);
}
/**  componentDidMount(){
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
**/
  render(){
    return(
      <>
      <Top/>
      <div>
        <>
        <div className='DatePicker bg-black bg-gradient'>
          <h1>Insira a data</h1>
          <input name="DataSolicitada" type="date"   className='Calendar' onChange={this.changeHandler}/>
          <div className="BotaoConfirma">
            <button type="submit" onClick={this.submitForm} className="block btn btn-outline-light">confirmar</button>
          </div>
        </div>
        </>
      </div>
      <Footer/>
    </>
    )
  }
}

export default App;
