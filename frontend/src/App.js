import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [password, setPassword] = useState('');
  const [complexity, setComplexity] = useState('medium');
  const [views, setViews] = useState(1);
  const [expirationDays, setExpirationDays] = useState(1);
  const [passwordUrl, setPasswordUrl] = useState('');

  const generatePassword = async () => {
    try {
      const response = await axios.post(
        'arn:aws:lambda:us-east-1:107887846702:function:gerenciamento_senhas',
        {
          complexity: complexity,
          views: views,
          expiration_days: expirationDays,
        }
      );
      setPasswordUrl(response.data.password_url);
    } catch (error) {
      console.error('Erro ao gerar senha:', error);
    }
  };

  return (
    <div className="App">
      <h1>Gerenciamento de Senhas</h1>
      <div>
        <label>
          Insira uma senha:
          <input
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Complexidade da senha:
          <select value={complexity} onChange={(e) => setComplexity(e.target.value)}>
            <option value="low">Baixa</option>
            <option value="medium">Média</option>
            <option value="high">Alta</option>
          </select>
        </label>
      </div>
      <div>
        <label>
          Quantas vezes a senha pode ser vista?
          <input
            type="number"
            value={views}
            onChange={(e) => setViews(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Quantos dias a senha ficará válida?
          <input
            type="number"
            value={expirationDays}
            onChange={(e) => setExpirationDays(e.target.value)}
          />
        </label>
      </div>
      <button onClick={generatePassword}>Gerar Senha</button>
      {passwordUrl && (
        <div>
          <p>URL para visualizar a senha:</p>
          <a href={passwordUrl} target="_blank" rel="noopener noreferrer">
            {passwordUrl}
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
