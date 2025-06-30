# PG_Workaholic

**Time-Based Blind SQLi**

---

### Scripts

- **`work.py`** – No threading  
  → Slower, more accurate
- **`work2.py`** – Threading enabled  
  → Faster, but may return NULLs or incorrect characters

---

### Usage

```bash
python work.py
# OR
python work2.py
```

---

### Proof of Concept

#### Database Name
![workaholic_1](../images/workaholic_1.png)  
![workaholic_2](../images/workaholic_2.png)

#### Current User
![workaholic_3](../images/workaholic_3.png)  
![workaholic_4](../images/workaholic_4.png)

#### Table Names
![workaholic_5](../images/workaholic_5.png)  
![workaholic_6](../images/workaholic_6.png)

#### Columns in a Table
![workaholic_7](../images/workaholic_7.png)  
![workaholic_8](../images/workaholic_8.png)

#### Row Values from Table & Column (Grabbing Users & Hashes)
![workaholic_9](../images/workaholic_9.png)  
![workaholic_10](../images/workaholic_10.png)  
![workaholic_11](../images/workaholic_11.png)  
![workaholic_12](../images/workaholic_12.png)
