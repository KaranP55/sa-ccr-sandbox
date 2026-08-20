{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "1173d895",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Product</th>\n",
       "      <th>Notional</th>\n",
       "      <th>Supervisory Duration</th>\n",
       "      <th>Maturity Factor</th>\n",
       "      <th>Supervisory Delta</th>\n",
       "      <th>Margined/Unmargined</th>\n",
       "      <th>Nettingset_ID</th>\n",
       "      <th>Hedgingset_ID</th>\n",
       "      <th>Effective Notional</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>IRS</td>\n",
       "      <td>1000000</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Margined</td>\n",
       "      <td>N1</td>\n",
       "      <td>NH1</td>\n",
       "      <td>1000000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Product  Notional  Supervisory Duration  Maturity Factor  Supervisory Delta  \\\n",
       "0     IRS   1000000                     1                1                  1   \n",
       "\n",
       "  Margined/Unmargined Nettingset_ID Hedgingset_ID  Effective Notional  \n",
       "0            Margined            N1           NH1             1000000  "
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "\n",
    "product1 = {\n",
    "            \"Product\" : \"IRS\",\n",
    "            \"Notional\": 1_000_000,\n",
    "            \"Supervisory Duration\":1,\n",
    "            \"Maturity Factor\":1,\n",
    "            \"Supervisory Delta\":1,\n",
    "            \"Margined/Unmargined\":\"Margined\",\n",
    "            \"Nettingset_ID\": \"N1\",\n",
    "            \"Hedgingset_ID\": \"NH1\"\n",
    "}\n",
    "\n",
    "df = pd.DataFrame([product1])\n",
    "\n",
    "df[\"Effective Notional\"]=df[\"Notional\"]*df[\"Supervisory Duration\"]*df[\"Maturity Factor\"]*df[\"Supervisory Delta\"]\n",
    "df\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e107127a",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "62f45960",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
