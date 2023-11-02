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
        DolarSolicitado: '',
        DolarAtual: '',
        Variacao: '',
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
    /** Procura e cadastra a cotação dolar e sua data , caso já exista no banco de dados não adiciona novamente*/
    axios.post(`http://localhost:8000/cotacao/${this.state.DataSolicitada}/`)
    .then((response) => {
      console.log("Cotação armazenada com sucesso",response)
    })
    .catch((error) => {
      console.error('Erro ao armazenar cotação:', error);
      this.setState({ DolarSolicitado: 'cotação inexistente' });
    })
    console.log(this.state);
    /** Busca o dolar no banco de dados por meio da API */
    axios.get(`http://localhost:8000/enviacotacao/${this.state.DataSolicitada}/`)
    .then((response) => {
      if(response.data.DolarSolicitado){
        this.setState({DolarSolicitado: response.data.DolarSolicitado.toFixed(2)});
        this.setState({DolarAtual: response.data.DolarAtual.toFixed(2)})
        const variacao = ((response.data.DolarAtual - response.data.DolarSolicitado) / response.data.DolarSolicitado) * 100;
        this.setState({ Variacao: variacao.toFixed(2)});
        console.log(response)
        }
      else{
        console.error('Falha ao obter cotação do Banco de Dados');
      }
    })
    .catch((error) => {
      console.error(`Erro: ${error}`);
    });
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
          <div className='Valores'>
            <h2 className='Valor'>{this.state.DolarSolicitado !== '' ? `Dólar Solicitado: R$ ${this.state.DolarSolicitado}` : 'Dólar Solicitado: '}</h2>
            <h2 className='Valor'>{this.state.DolarAtual !== '' ? `Dólar Atual: R$ ${this.state.DolarAtual}` : 'Dólar Atual: '}</h2>
            <h2 className='Valor'>{this.state.Variacao !== '' ? `Variação: ${this.state.Variacao}%` : 'Variação : '}</h2>
            <h2 className='Valor'>Variação significativa :</h2>
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
