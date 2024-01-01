// auth.js
const auth = firebase.auth();

// ユーザー登録
function signUp() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  auth.createUserWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // 登録成功
      const user = userCredential.user;
      console.log('User created:', user);
    })
    .catch((error) => {
      // エラー処理
      console.error('Sign up error:', error);
    });
}

// ユーザーログイン
function signIn() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  auth.signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // ログイン成功
      const user = userCredential.user;
      console.log('User signed in:', user);
    })
    .catch((error) => {
      // エラー処理
      console.error('Sign in error:', error);
    });
}
