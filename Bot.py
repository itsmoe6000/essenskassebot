{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "af0d2c13-07b2-428a-be65-018ac91a41ad",
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "import pandas as pd\n",
    "from datetime import datetime\n",
    "from telegram import Update\n",
    "from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters\n",
    "\n",
    "# Datenstruktur zum Speichern der Beträge\n",
    "data = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "9f41e1ae-61a4-4346-b89e-e42795d67e0b",
   "metadata": {},
   "outputs": [],
   "source": [
    "async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):\n",
    "    global data\n",
    "    message = update.message.text\n",
    "    user = update.message.from_user.username or update.message.from_user.first_name\n",
    "\n",
    "    # Debug: Eingehende Nachricht anzeigen\n",
    "    print(f\"Empfangene Nachricht: {message}\")\n",
    "\n",
    "    # Suche nach Geldbeträgen mit verbessertem Regex\n",
    "    pattern = r\"(\\d+(?:[\\.,]\\d{1,2})?)\\s?(€|EUR|USD|CHF)?\"\n",
    "    match = re.search(pattern, message)\n",
    "\n",
    "    if match:\n",
    "        # Debug: Gefundene Gruppen anzeigen\n",
    "        print(f\"Gefundener Betrag: {match.group(1)}\")\n",
    "        print(f\"Gefundene Währung: {match.group(2)}\")\n",
    "\n",
    "        # Betrag und Währung extrahieren\n",
    "        amount = float(match.group(1).replace(\",\", \".\"))\n",
    "        currency = match.group(2) or \"EUR\"\n",
    "\n",
    "        # Daten speichern\n",
    "        data.append({\n",
    "            \"user\": user,\n",
    "            \"amount\": amount,\n",
    "            \"currency\": currency,\n",
    "            \"date\": datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")\n",
    "        })\n",
    "\n",
    "        # Debug: Aktuelle Daten anzeigen\n",
    "        print(f\"Aktuelle Daten: {data}\")\n",
    "\n",
    "        await update.message.reply_text(f\"{user}, ich habe {amount} {currency} gespeichert!\")\n",
    "    else:\n",
    "        # Debug: Regex hat nichts gefunden\n",
    "        print(f\"Regex hat keinen Betrag gefunden. Nachricht: {message}\")\n",
    "        await update.message.reply_text(\"Kein gültiger Betrag erkannt.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "230a0841-0867-4768-9d70-9926de56e0e0",
   "metadata": {},
   "outputs": [],
   "source": [
    "async def summary_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):\n",
    "    global data\n",
    "\n",
    "    if not data:\n",
    "        await update.message.reply_text(\"Keine Daten vorhanden.\")\n",
    "        return\n",
    "\n",
    "    # Erstelle einen DataFrame aus den Daten\n",
    "    df = pd.DataFrame(data)\n",
    "    df['date'] = pd.to_datetime(df['date'])\n",
    "    df['month'] = df['date'].dt.to_period('M')\n",
    "\n",
    "    # Summiere die Beträge\n",
    "    summary = df.groupby(['user', 'month', 'currency'])['amount'].sum().reset_index()\n",
    "\n",
    "    # Ausgabe formatieren\n",
    "    summary_text = \"\\\\nZusammenfassung pro Person und Monat:\\\\n\"\n",
    "    for _, row in summary.iterrows():\n",
    "        summary_text += f\"{row['user']} - {row['month']} - {row['amount']:.2f} {row['currency']}\\\\n\"\n",
    "    print(data)\n",
    "    await update.message.reply_text(summary_text)\n",
    "   "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "79cebe11-04cc-419c-9134-f068eb82711f",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "import nest_asyncio\n",
    "import asyncio\n",
    "from telegram import Bot\n",
    "\n",
    "# nest_asyncio aktivieren\n",
    "nest_asyncio.apply()\n",
    "\n",
    "# Bot-Token\n",
    "TOKEN = \"7609808796:AAH1BgMYmjHRbDbn5ouhnrGcSuvuYajOr5I\"\n",
    "bot = Bot(token=TOKEN)\n",
    "\n",
    "# Chat-ID der Gruppe\n",
    "CHAT_ID = \"2449977748\"\n",
    "\n",
    "# Abrufen der Nachrichten aus der Chathistory\n",
    "async def fetch_chat_history():\n",
    "    updates = await bot.get_updates()  # Abrufen neuer Nachrichten\n",
    "    for update in updates:\n",
    "        # Überprüfe, ob die Nachricht aus der richtigen Gruppe stammt\n",
    "        if update.message and update.message.chat.id == CHAT_ID:\n",
    "            print(f\"Nachricht: {update.message.text} von {update.message.from_user.username}\")\n",
    "\n",
    "# Event-Loop verwenden\n",
    "await fetch_chat_history()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "214ba320-f52f-47c4-9b5b-4bed2ac56d56",
   "metadata": {},
   "source": [
    "# Executing the bot"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "8ef1931a-012a-427f-8cd4-c50416a11f4d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Bot läuft...\n",
      "Empfangene Nachricht: 30€\n",
      "Gefundener Betrag: 30\n",
      "Gefundene Währung: €\n",
      "Aktuelle Daten: [{'user': 'Moses', 'amount': 30.0, 'currency': '€', 'date': '2025-01-25 21:04:24'}]\n",
      "Empfangene Nachricht: 20.e\n",
      "Gefundener Betrag: 20\n",
      "Gefundene Währung: None\n",
      "Aktuelle Daten: [{'user': 'Moses', 'amount': 30.0, 'currency': '€', 'date': '2025-01-25 21:04:24'}, {'user': 'Moses', 'amount': 20.0, 'currency': 'EUR', 'date': '2025-01-25 21:04:29'}]\n",
      "[{'user': 'Moses', 'amount': 30.0, 'currency': '€', 'date': '2025-01-25 21:04:24'}, {'user': 'Moses', 'amount': 20.0, 'currency': 'EUR', 'date': '2025-01-25 21:04:29'}]\n"
     ]
    },
    {
     "ename": "RuntimeError",
     "evalue": "Cannot close a running event loop",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mRuntimeError\u001b[0m                              Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[6], line 21\u001b[0m\n\u001b[1;32m     19\u001b[0m \u001b[38;5;66;03m# Starten\u001b[39;00m\n\u001b[1;32m     20\u001b[0m \u001b[38;5;28mprint\u001b[39m(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mBot läuft...\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[0;32m---> 21\u001b[0m \u001b[38;5;28;01mawait\u001b[39;00m app\u001b[38;5;241m.\u001b[39mrun_polling()\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/telegram/ext/_application.py:868\u001b[0m, in \u001b[0;36mApplication.run_polling\u001b[0;34m(self, poll_interval, timeout, bootstrap_retries, read_timeout, write_timeout, connect_timeout, pool_timeout, allowed_updates, drop_pending_updates, close_loop, stop_signals)\u001b[0m\n\u001b[1;32m    865\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21merror_callback\u001b[39m(exc: TelegramError) \u001b[38;5;241m-\u001b[39m\u001b[38;5;241m>\u001b[39m \u001b[38;5;28;01mNone\u001b[39;00m:\n\u001b[1;32m    866\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mcreate_task(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mprocess_error(error\u001b[38;5;241m=\u001b[39mexc, update\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mNone\u001b[39;00m))\n\u001b[0;32m--> 868\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m__run(\n\u001b[1;32m    869\u001b[0m     updater_coroutine\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mupdater\u001b[38;5;241m.\u001b[39mstart_polling(\n\u001b[1;32m    870\u001b[0m         poll_interval\u001b[38;5;241m=\u001b[39mpoll_interval,\n\u001b[1;32m    871\u001b[0m         timeout\u001b[38;5;241m=\u001b[39mtimeout,\n\u001b[1;32m    872\u001b[0m         bootstrap_retries\u001b[38;5;241m=\u001b[39mbootstrap_retries,\n\u001b[1;32m    873\u001b[0m         read_timeout\u001b[38;5;241m=\u001b[39mread_timeout,\n\u001b[1;32m    874\u001b[0m         write_timeout\u001b[38;5;241m=\u001b[39mwrite_timeout,\n\u001b[1;32m    875\u001b[0m         connect_timeout\u001b[38;5;241m=\u001b[39mconnect_timeout,\n\u001b[1;32m    876\u001b[0m         pool_timeout\u001b[38;5;241m=\u001b[39mpool_timeout,\n\u001b[1;32m    877\u001b[0m         allowed_updates\u001b[38;5;241m=\u001b[39mallowed_updates,\n\u001b[1;32m    878\u001b[0m         drop_pending_updates\u001b[38;5;241m=\u001b[39mdrop_pending_updates,\n\u001b[1;32m    879\u001b[0m         error_callback\u001b[38;5;241m=\u001b[39merror_callback,  \u001b[38;5;66;03m# if there is an error in fetching updates\u001b[39;00m\n\u001b[1;32m    880\u001b[0m     ),\n\u001b[1;32m    881\u001b[0m     close_loop\u001b[38;5;241m=\u001b[39mclose_loop,\n\u001b[1;32m    882\u001b[0m     stop_signals\u001b[38;5;241m=\u001b[39mstop_signals,\n\u001b[1;32m    883\u001b[0m )\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/site-packages/telegram/ext/_application.py:1099\u001b[0m, in \u001b[0;36mApplication.__run\u001b[0;34m(self, updater_coroutine, stop_signals, close_loop)\u001b[0m\n\u001b[1;32m   1097\u001b[0m \u001b[38;5;28;01mfinally\u001b[39;00m:\n\u001b[1;32m   1098\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m close_loop:\n\u001b[0;32m-> 1099\u001b[0m         loop\u001b[38;5;241m.\u001b[39mclose()\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/asyncio/unix_events.py:68\u001b[0m, in \u001b[0;36m_UnixSelectorEventLoop.close\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m     67\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mclose\u001b[39m(\u001b[38;5;28mself\u001b[39m):\n\u001b[0;32m---> 68\u001b[0m     \u001b[38;5;28msuper\u001b[39m()\u001b[38;5;241m.\u001b[39mclose()\n\u001b[1;32m     69\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m sys\u001b[38;5;241m.\u001b[39mis_finalizing():\n\u001b[1;32m     70\u001b[0m         \u001b[38;5;28;01mfor\u001b[39;00m sig \u001b[38;5;129;01min\u001b[39;00m \u001b[38;5;28mlist\u001b[39m(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_signal_handlers):\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.12/asyncio/selector_events.py:101\u001b[0m, in \u001b[0;36mBaseSelectorEventLoop.close\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m     99\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mclose\u001b[39m(\u001b[38;5;28mself\u001b[39m):\n\u001b[1;32m    100\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mis_running():\n\u001b[0;32m--> 101\u001b[0m         \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mRuntimeError\u001b[39;00m(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mCannot close a running event loop\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[1;32m    102\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mis_closed():\n\u001b[1;32m    103\u001b[0m         \u001b[38;5;28;01mreturn\u001b[39;00m\n",
      "\u001b[0;31mRuntimeError\u001b[0m: Cannot close a running event loop"
     ]
    }
   ],
   "source": [
    "from telegram.ext import ApplicationBuilder, Application\n",
    "\n",
    "TOKEN = \"7609808796:AAH1BgMYmjHRbDbn5ouhnrGcSuvuYajOr5I\"  # Ersetze mit deinem Bot-Token\n",
    "\n",
    "# Bot-Anwendung erstellen\n",
    "app = ApplicationBuilder().token(TOKEN).build()\n",
    "\n",
    "# Handler hinzufügen\n",
    "app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))\n",
    "app.add_handler(CommandHandler(\"summary\", summary_handler))\n",
    "\n",
    "# Bot in Jupyter kompatibel starten\n",
    "import nest_asyncio\n",
    "import asyncio\n",
    "\n",
    "# Nest AsyncIO aktivieren (nur in Jupyter notwendig)\n",
    "nest_asyncio.apply()\n",
    "\n",
    "# Starten\n",
    "print(\"Bot läuft...\")\n",
    "await app.run_polling()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0d9b9fa8-b247-45d6-a61f-be96b60c44c5",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "cf07e4ef-3dd3-420c-bc16-bae8a7418483",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
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
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
