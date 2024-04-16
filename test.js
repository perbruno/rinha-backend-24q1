test_case = [
  {
    client_id: 1,
    route: "transacoes",
    method: "POST",
    data: {
      valor: 99990000,
      tipo: "d",
      descricao: "limiteAlto",
    },
    expected: {
      status: 422,
      message: null,
    },
  },
  {
    client_id: 6,
    route: "extrato",
    method: "GET",
    data: {
      valor: 99990000,
      tipo: "d",
      descricao: "noUser1",
    },
    expected: {
      status: 404,
      message: null,
    },
  },
  {
    client_id: 6,
    route: "transacoes",
    method: "POST",
    data: {
      valor: 99990000,
      tipo: "d",
      descricao: "noUser2",
    },
    expected: {
      status: 404,
      message: null,
    },
  },
  {
    client_id: 6,
    route: "transacoes",
    method: "POST",
    data: {
      valor: -12354,
      tipo: "d",
      descricao: "negativeNum",
    },
    expected: {
      status: 422,
      message: null,
    },
  },
  {
    client_id: 1,
    route: "transacoes",
    method: "POST",
    data: {
      valor: 12354,
      tipo: "G",
      descricao: "wrongType",
    },
    expected: {
      status: 422,
      message: null,
    },
  },
  {
    client_id: 3,
    route: "extrato",
    method: "GET",
    data: {},
    expected: {
      status: 200,
      message: null,
    },
  },
  {
    client_id: 3,
    route: "transacoes",
    method: "POST",
    data: {
      valor: Math.floor(Math.random() * 10000),
      tipo: Math.random() < 0.5 ? "d" : "c",
      descricao: "valid1",
    },
    expected: {
      status: 200,
      message: null,
    },
  },
  {
    client_id: 3,
    route: "transacoes",
    method: "POST",
    data: {
      valor: Math.floor(Math.random() * 10000),
      tipo: Math.random() < 0.5 ? "d" : "c",
      descricao: "valid2",
    },
    expected: {
      status: 200,
      message: null,
    },
  },
  {
    client_id: 3,
    route: "transacoes",
    method: "POST",
    data: {
      valor: Math.floor(Math.random() * 10000),
      tipo: Math.random() < 0.5 ? "d" : "c",
      descricao: "valid3",
    },
    expected: {
      status: 200,
      message: null,
    },
  },
  {
    client_id: 3,
    route: "transacoes",
    method: "POST",
    data: {
      valor: Math.floor(Math.random() * 10000),
      tipo: Math.random() < 0.5 ? "d" : "c",
      descricao: "valid4",
    },
    expected: {
      status: 200,
      message: null,
    },
  },
  {
    client_id: 3,
    route: "transacoes",
    method: "POST",
    data: {
      valor: Math.floor(Math.random() * 10000),
      tipo: Math.random() < 0.5 ? "d" : "c",
      descricao: "valid5",
    },
    expected: {
      status: 200,
      message: null,
    },
  },
  {
    client_id: 3,
    route: "extrato",
    method: "GET",
    data: {},
    expected: {
      status: 200,
      message: null,
    },
  },
];

// Define the API URL
const apiUrl = "http://localhost:9999/clientes";

for (let index = 0; index < test_case.length; index++) {
  const test = test_case[index];
  let requestOptions;
  if (test.method == "POST") {
    requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(test.data),
    };
  } else {
    requestOptions = {
      method: "GET",
    };
  }

  fetch(`${apiUrl}/${test.client_id}/${test.route}`, requestOptions)
    .then((response) => {
      console.log(test);
      console.log("response status", response.status);
      console.log(response.status == test.expected.status);
      return response.json();
    })
    .then((data) => {
      console.log(JSON.stringify(data, null, 2));
    })
    .catch((error) => {
      console.error("Error:", error.message);
    });
}
