import streamlit as st
import datetime
import json
import os

def teacher_match(option):
    teachers = {
        "1": "ผศ.ดร.ชีวัน", "2": "อ.ณัฐธิดา", "3": "อ.อรทัย", "4": "อ.จิตต์ตรา",
        "5": "อ.กฤตเมธ", "6": "อ.ณัฐนันท์", "7": "อ.ฤทธิชัย", "8": "อ.ชวลิต",
        "9": "อ.พหุกร", "10": "อ.คมสันต์", "11": "อ.ธีรภัทร", "12": "อ.ชนัยสุดา",
        "13": "อ.สุรางค์", "14": "อ.กัญจ์พสิษฐ์", "15": "อ.ดร.ณัฐ", "16": "Aj.jessica",
        "17": "อ.สิริกุล", "18": "อ.ณภัสวรรก์"
    }
    return teachers.get(option, "Invalid option")

def load_homework():
    try:
        with open('homework.json', 'r') as f:
            data = f.read()
            if not data:
                return []
            return json.loads(data)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_homework(homework_list):
    with open('homework.json', 'w') as f:
        json.dump(homework_list, f)

def main():
    st.set_page_config(page_title="ระบบจัดการการบ้าน", page_icon="📚", layout="wide")
    
    dark_mode = st.sidebar.checkbox("Dark Mode")
    
    if dark_mode:
        st.markdown(
            """
            <style>
            body {
                color: #E0E0E0;
                background-color: #1E1E1E;
            }
            .stApp {
                background-color: #1E1E1E;
            }
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > div,
            .stDateInput > div > div > input {
                color: #E0E0E0;
                background-color: #2D2D2D;
            }
            .stButton > button {
                color: #E0E0E0;
                background-color: #3D3D3D;
                border: none;
            }
            .stButton > button:hover {
                background-color: #4D4D4D;
            }
            h1, h2, h3, label, .stSelectbox label, .stTextArea label, .stDateInput label {
                color: #FFFFFF !important;
            }
            .stAlert {
                background-color: #2D2D2D;
                color: #E0E0E0;
            }
            .stDateInput > div > div {
                background-color: #000000;
                border: 1px solid #FFFFFF;
            }
            .stDateInput input {
                color: #E0E0E0 !important;
                background-color: #000000 !important;
            }
            .stSidebar {
                background-color: #1E1E1E;
            }
            @media (max-width: 768px) {
                .stApp {
                    padding: 1rem;
                }
                .stTextInput > div > div > input,
                .stTextArea > div > div > textarea,
                .stSelectbox > div > div > div,
                .stDateInput > div > div > input {
                    font-size: 14px;
                }
                h1 {
                    font-size: 24px;
                }
                h2 {
                    font-size: 20px;
                }
                h3 {
                    font-size: 18px;
                }
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
    st.title("ระบบจัดการการบ้าน 📚")

    if 'homework_list' not in st.session_state:
        st.session_state.homework_list = load_homework()

    container = st.container()

    with container:
        st.subheader("เพิ่มการบ้านใหม่")
        subject_options = {
            "1": "นาฎศิลป์", "2": "ดนตรีสากล", "3": "คณิต A", "4": "ห้องสมุด",
            "5": "พละ", "6": "ภาษาไทย", "7": "สังคมศึกษา", "8": "คณิต B",
            "9": "สุขศึกษา", "10": "ศิลปะ", "11": "พระพุทธ", "12": "ไทยเพิ่มเติม",
            "13": "วิทย์", "14": "ประวัติศาสตร์", "15": "คณิตเพิ่มเติม",
            "16": "อังกฤษ(jessica)", "17": "อังกฤษ(อ.สิริกุล)", "18": "technology"
        }
        option = st.selectbox("เลือกวิชา", options=list(subject_options.keys()), format_func=lambda x: subject_options[x])
        teacher = teacher_match(option)
        text = st.text_area("เนื้อหาการบ้าน")
        due_date = st.date_input("วันที่ส่งการบ้าน")

        if st.button("เพิ่มการบ้าน"):
            if teacher != "Invalid option" and text and due_date:
                st.session_state.homework_list.append({
                    "subject": subject_options[option],
                    "teacher": teacher,
                    "text": text,
                    "due_date": due_date.strftime('%Y-%m-%d'),
                    "assigned_date": datetime.datetime.now().strftime('%Y-%m-%d')
                })
                save_homework(st.session_state.homework_list)
                st.success("เพิ่มการบ้านเรียบร้อยแล้ว!")
            else:
                st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

        st.subheader("รายการการบ้านทั้งหมด")
        if st.session_state.homework_list:
            today = datetime.datetime.now()
            output = f"จดการบ้าน 📕《{today.strftime('%d %b %Y')}》\n"
            output += "======================\n"
            for i, homework in enumerate(st.session_state.homework_list):
                output += f"#{homework['subject']}\n"
                output += f"-{homework['text']}\n"
                due_date = datetime.datetime.strptime(homework['due_date'], '%Y-%m-%d')
                output += f"[{due_date.strftime('%d %b %Y')}]" + "{" + f"{homework['teacher']}" + "}\n"
            output += "******************************"
            st.text_area("รายละเอียดการบ้าน", value=output, height=300)

            st.subheader("ลบการบ้าน")
            homework_to_remove = st.selectbox("เลือกการบ้านที่ต้องการลบ", 
                                              options=range(len(st.session_state.homework_list)),
                                              format_func=lambda x: f"{st.session_state.homework_list[x]['subject']} - {st.session_state.homework_list[x]['text'][:30]}...")
            if st.button("ลบการบ้าน"):
                removed_homework = st.session_state.homework_list.pop(homework_to_remove)
                save_homework(st.session_state.homework_list)
                st.success(f"ลบการบ้าน '{removed_homework['subject']}' เรียบร้อยแล้ว!")
        else:
            st.info("ยังไม่มีการบ้าน")

if __name__ == "__main__":
    main()
