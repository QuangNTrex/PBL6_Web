
import axios from "axios";
import VerifyCode from "../auth/VerifyCode";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

function VerifyPage() {
    const user = useSelector(state => state.user)
    const navigate = useNavigate()
    // console.log(user)
  const handleVerify = async (code) => {
    try {
      const res = await axios.post(`http://localhost:8000/auth/verify-code?email=${user.email}&code=${code}`,);
      console.log(res)
      navigate("/")
      alert("Xác minh thành công!");
    } catch (err) {
      alert("Mã không đúng hoặc đã hết hạn!");
      console.log(err)
    }
  };

  return <VerifyCode onVerify={handleVerify} />;
}

export default VerifyPage;
