if submit_btn:
            if name.strip() != "":
                dialects_text = ", ".join(dialects) if dialects else "عادية"
                
                # ---- ضيف هذول السطور هون ----
                import requests
                GOOGLE_SCRIPT_URL = "الصق_رابطك_السحري_هون"
                
                payload = {
                    "الاسم": name, "العمر": age, "الجنس": gender, 
                    "المظهر": appearance, "نوع الدور": role_type, 
                    "اللهجات": dialects_text, "رقم الهاتف": phone, "رابط الفيديو": video_link
                }
                try:
                    requests.post(GOOGLE_SCRIPT_URL, json=payload)
                except:
                    pass
                # -----------------------------
                
                new_row = pd.DataFrame({
                    'الاسم': [name], 
                    'العمر': [age], 
                    'الجنس': [gender], 
                    'المظهر': [appearance], 
                    'نوع الدور': [role_type], 
                    'اللهجات': [dialects_text],
                    'رقم الهاتف': [phone],
                    'رابط الفيديو': [video_link]
                })
                st.session_state.actors_data = pd.concat([st.session_state.actors_data, new_row], ignore_index=True)
                st.success(f"تم إرسال طلبك بنجاح يا {name}!")
            else:
                st.error("الرجاء إدخال الاسم على الأقل.")
