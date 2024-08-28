# Alp Onder Yener, Ada Yilmaz, Efe Kilickaya, Efe Guclu

import socket
import threading
import tkinter as tk
import time
from collections import defaultdict
from copy import deepcopy

class ServerApp: # Server class
    def __init__(self, master):
        self.master = master # Setup GUI
        self.master.title("Server")

        tk.Label(master, text="Port:").pack()  # port entry
        self.port_entry = tk.Entry(master)
        self.port_entry.pack()

        self.start_button = tk.Button(  # start server button
            master, text="Start Server", command=self.start_server
        )
        self.start_button.pack()

        self.system_messages = tk.Text( # Where system messages will be displayed
            master, state="disabled", height=10, width=50
        )  # display messages
        self.system_messages.pack()

        tk.Label(master, text="Players:").pack()  # display player list / leaderboard
        self.players_list = tk.Text(master, state="disabled", height=10, width=50)
        self.players_list.pack()

        self.players = {} #dictionary to store connected players. key = name, value = socket
        self.capacity = 4 #number of players
        self.queue = {}  #dictionary for queue. same structure as players dict
        self.queue_order = [] #to keep the order of the queue first element will have the name of the player to be.
        self.choices = {} # holds the choices made during the game
        self.eliminated = {} #holds eliminated players to put them back in the game on restart

    def broadcast(self, message): #broadcast a message to players
        for player_socket in self.players.values():
            try:
                player_socket.send(message.encode("utf-8"))

            except Exception as e:
                self.log_system_message(
                    f"Error sending message to {player_socket}: {e}"
                )

    def broadcast_all(self, message): #broadcast a message to all clients: players, queue, eliminated
        for player_socket in self.players.values():
            try:
                player_socket.send(message.encode("utf-8"))

            except Exception as e:
                self.log_system_message(
                    f"Error sending message to {player_socket}: {e}"
                )

        for player_socket in self.queue.values():
            try:
                player_socket.send(message.encode("utf-8"))

            except Exception as e:
                self.log_system_message(
                    f"Error sending message to {player_socket}: {e}"
                )

        for player_socket in self.eliminated.values():
            try:
                player_socket.send(message.encode("utf-8"))

            except Exception as e:
                self.log_system_message(
                    f"Error sending message to {player_socket}: {e}"
                )

    def broadcast_game(self, message): #broadcast a message to players + eliminated
        for player_socket in self.players.values():
            try:
                player_socket.send(message.encode("utf-8"))

            except Exception as e:
                self.log_system_message(
                    f"Error sending message to {player_socket}: {e}"
                )

        for player_socket in self.eliminated.values():
            try:
                player_socket.send(message.encode("utf-8"))

            except Exception as e:
                self.log_system_message(
                    f"Error sending message to {player_socket}: {e}"
                )

    def log_system_message(self, message): #server log messages
        self.system_messages.config(state="normal")
        self.system_messages.insert(tk.END, message + "\n")
        self.system_messages.yview(tk.END)
        self.system_messages.config(state="disabled")

    def update_players_list_after_game(self, winner_name): #updates scoreboard by adding +1 to the winner
        self.players_list.config(state="normal")
        self.players_list.delete(1.0, tk.END)

        with open("leaderboard.txt", "r+") as file:
            leaderboard_lines = file.readlines()

        entries = []

        for name in self.players.keys():
            matched_line = next(
                    (line for line in leaderboard_lines if line.strip().split()[0] == name),
                None,
            )
            if (matched_line):  #if name found in leaderboard, display the whole line in system messages
                name, score_str = matched_line.strip().split()
                score = int(score_str)  # Convert score to integer for sorting
                if winner_name == name:
                    score += 1
                entries.append((name, score))

        for name in self.eliminated.keys(): #do the same for eliminateds
            matched_line = next(
                (line for line in leaderboard_lines if line.strip().split()[0] == name),
            None,
        )
            if matched_line:
                name, score_str = matched_line.strip().split()
                score = int(score_str)  #convert score to integer for sorting
                entries.append((name, score))
                self.players[name] = self.eliminated[name]  #add back to players dictionary

        self.eliminated = {}  #clear eliminated players for a new game

        entries.sort(key=lambda x: x[1], reverse=True) #sort entries according to their wins

        leaderboard_to_clients = f"LEADERBOARD"
        for name, score in entries:
            self.players_list.insert(tk.END, f"{name} {score}\n")
            leaderboard_to_clients += f"{name} {score}\n"

        self.broadcast_all(leaderboard_to_clients) #broadcast the leaderboard to clients

        self.players_list.yview(tk.END)
        self.players_list.config(state="disabled")

        with open("leaderboard.txt", "w") as file:
            file.writelines(leaderboard_to_clients[11:])

    def update_players_list(self): #regular update before the game when new players are added
        self.players_list.config(state="normal")
        self.players_list.delete(1.0, tk.END)

        with open("leaderboard.txt", "r+") as file:
            leaderboard_lines = file.readlines()

        entries = []

        updated = False
        for name in self.players.keys():
            matched_line = next(
                (line for line in leaderboard_lines if line.strip().split()[0] == name),
                None,
            )
            if (matched_line):  #if name found in leaderboard, display the whole line in system messages
                name, score_str = matched_line.strip().split()
                score = int(score_str)  #convert score to integer for sorting
                entries.append((name, score))

            else:  #if name not found, add name with score 0 to system messages and leaderboard
                new_entry = f"{name} 0\n"
                entries.append((name, 0))
                leaderboard_lines.append(new_entry)  #prepare new entry for file update
                updated = True

        entries.sort(key=lambda x: x[1], reverse=True) #sort according to their wins

        leaderboard_to_clients = f"LEADERBOARD"
        for name, score in entries:
            self.players_list.insert(tk.END, f"{name} {score}\n")
            leaderboard_to_clients += f"{name} {score}\n"

        self.broadcast_all(leaderboard_to_clients) #broadcast to clients
        self.players_list.yview(tk.END)
        self.players_list.config(state="disabled")

        if updated: #update leaderboard.txt
            with open("leaderboard.txt", "w") as file:
                file.writelines(leaderboard_lines)

    def start_game(self): #start the game with the countdown and appropriate message
        for key, value in self.eliminated:
            self.players[key] = value
        self.eliminated = {}

        time.sleep(0.2)
        self.broadcast("The game will start in 5 seconds.")
        self.log_system_message(f"The game will start in 5 seconds.")
        countdown = [5, 4, 3, 2, 1]

        for count in countdown:
            if(len(self.players) < self.capacity): #if players leave the game during countdown, stop and restart with new players from queue
                self.broadcast_all("Not enough players. Restarting the game.")
                self.log_system_message("Not enough players. Restarting the game.")
                self.restart_game()

            self.broadcast(str(count))
            self.log_system_message(str(count))
            time.sleep(1)

        self.broadcast("Go!")
        time.sleep(0.1)
        self.broadcast("Pick a move, you have 10 seconds.")
        self.log_system_message(f"The game has started.")

    def restart_game(self): #set the game up for the next game
        while(len(self.players) < self.capacity):
            if(len(self.queue) > 0): #if queue is not empty, get the first one to join the game
                next_player = self.queue_order.pop(0)
                self.queue[next_player].send("You are now in the game!".encode("utf-8"))
                self.players[next_player] = self.queue[next_player]
                del self.queue[next_player]
                self.update_players_list()
            else:
                break

        if(len(self.players) == self.capacity): self.start_game() #start the game if capacity is reached
        else: self.broadcast("Waiting for more players...")
    
    def find_name_from_socket(self, socket): #gets the name of the user with the given socket value
        for key, val in self.players.items():
            if val == socket:
                return key
        for key, val in self.queue.items():
            if val == socket:
                return key
        for key, val in self.eliminated.items():
            if val == socket:
                return key
        return
    
    def count_keys_with_same_value(self, dictionary): #how many of each value does a dictionary contain
        value_to_keys = defaultdict(list)
        for key, value in dictionary.items(): #populate the value_to_keys dictionary
            value_to_keys[value].append(key)
        
        counts = {value: len(keys) for value, keys in value_to_keys.items()}#count the keys for each value
        return counts

    def all_values_nonzero(self, dictionary): #check if all values of a dictionary are non zero -results in tie
        return all(value != 0 for value in dictionary.values()) and len(dictionary) == 3

    def find_opponents(self, gesture): #seperate into winners and losers
        if gesture == "R":
            return "P", "S"
        if gesture == "P":
            return "S", "R"
        if gesture == "S":
            return "R", "P"

    def evaluate_results(self): #check who the winner is
        actual_choices = deepcopy(self.choices)
        gesture_counts = self.count_keys_with_same_value(actual_choices)
        all_gestures_made = self.all_values_nonzero(gesture_counts)
        
        if all_gestures_made:
            return "TIE"
        
        if sum(gesture_counts.values()) == 4:
            for gesture, count in gesture_counts.items(): #check for 3v1
                if count == 3:
                    win, lose = self.find_opponents(gesture)
                    for gesture2, count2 in gesture_counts.items():
                        if count2 == 1 and gesture2 != gesture:
                            if gesture2 == win:
                                return gesture2
                            elif gesture2 == lose:
                                return gesture
            
            for gesture, count in gesture_counts.items(): #check for 2v2
                if count == 2:
                    win, lose = self.find_opponents(gesture)
                    for gesture2, count2 in gesture_counts.items():
                        if count2 == 2 and gesture2 != gesture:
                            if gesture2 == win:
                                return gesture2
                            elif gesture2 == lose:
                                return gesture
            
            for gesture, count in gesture_counts.items(): #check for all same choice
                if count == 4:
                    return "TIE"
                
        elif sum(gesture_counts.values()) == 3:
            for gesture, count in gesture_counts.items(): #check for 2v1
                if count == 2:
                    win, lose = self.find_opponents(gesture)
                    for gesture2, count2 in gesture_counts.items():
                        if count2 == 1 and gesture2 != gesture:
                            if gesture2 == win:
                                return gesture2
                            elif gesture2 == lose:
                                return gesture
            
            for gesture, count in gesture_counts.items(): #check for all same choice
                if count == 3:
                    return "TIE"

        elif sum(gesture_counts.values()) == 2:
            for gesture, count in gesture_counts.items(): #check for 1v1
                if count == 1:
                    win, lose = self.find_opponents(gesture)
                    for gesture2, count2 in gesture_counts.items():
                        if count2 == 1 and gesture2 != gesture:
                            if gesture2 == win:
                                return gesture2
                            elif gesture2 == lose:
                                return gesture
            
            for gesture, count in gesture_counts.items(): # check for all same choice
                if count == 2:
                    return "TIE"
        
        elif sum(gesture_counts.values()) == 1:
            for gesture, count in gesture_counts.items(): # check for 1v1
                if count == 1:
                    return gesture
                
    def handle_client(self, client_socket, address): #receive messages from the clients
        self.log_system_message(f"Client {address} connected.")
        name = None

        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if message.startswith("NAME:"):  #if a new name message is incoming from the client
                    name = message.split(":")[1]

                    if name in self.players.keys() or name in self.queue.keys():
                        client_socket.send("Name already taken.".encode("utf-8"))
                        continue

                    elif (len(self.players) <= self.capacity):  #if the player count is not sufficient, wait for other players
                        self.players[name] = client_socket
                        client_socket.send(f"You are in the game, {name}!".encode("utf-8"))
                        self.log_system_message(f"{name} is in the game.")
                        self.update_players_list()

                        if len(self.players) == self.capacity:
                            time.sleep(0.2)
                            self.start_game()

                    else:  # Add to queue
                        self.queue[name] = client_socket
                        self.queue_order.append(name)
                        client_socket.send("The room is full.".encode("utf-8"))
                        self.log_system_message(f"{name} is in the queue.")

                elif message == "LEAVE":  #client clicked leave button

                    if name in self.players.keys():
                        del self.players[name]
                        self.log_system_message(f"{name} left the game.")
                        self.broadcast(f"{name} left the game.")
                        self.update_players_list()

                    elif name in self.queue:
                        del self.queue[name]
                        self.queue_order.remove(name)
                        self.log_system_message(f"{name} left the game.")
                        self.broadcast(f"{name} left the game.")

                    break  #exit the loop since the client is leaving

                elif message == "GAME":
                    
                    self.choices = {}
                    player_choice = ""
                    time.sleep(0.5) #so that threads don't get tangled
                    
                    player_name = self.find_name_from_socket(client_socket)
                    start_time = time.time()

                    if player_name not in self.eliminated:
                        while(time.time() - start_time <= 10):
                            if(len(self.players) == 1) and player_name in self.players: 
                                client_socket.send("Everyone else left the game. YOU WON!".encode("utf-8"))
                                self.broadcast_all(f"{player_name} has won the game! New game coming up...")
                                self.log_system_message(f"{player_name} has won the game! New game coming up...")

                                self.players.update(self.eliminated) #add the eliminated players back to players dict
                                time.sleep(0.1)
                                self.update_players_list_after_game(winner_name)
                                time.sleep(0.1)
                                self.restart_game()
                                break

                            elif(player_choice == ""):
                                try:
                                    client_socket.settimeout(10 - (time.time() - start_time))
                                    player_choice = client_socket.recv(1024).decode("utf-8").split(":")[1]

                                    self.log_system_message(player_name + " has picked choice " + player_choice)
                                    self.choices[player_name] = player_choice
                                except socket.timeout:
                                    continue

                            else:
                                if(len(self.choices) == len(self.players)):
                                    break #wait until all players have chosen 


                        if(player_choice == ""): #if 10 sec has passed, eliminate the player
                            client_socket.send("10 seconds have passed. YOU LOST.".encode("utf-8"))
                            self.log_system_message(f"{name} is eliminated.")
                            self.eliminated[player_name] = client_socket
                            del self.players[player_name]

                    time.sleep(0.1)

                    if(len(self.players) == 0): #if everyone was eliminated, start a new game
                        client_socket.send("YOU LOST.".encode("utf-8")) 
                        self.broadcast_all("All players have been eliminated. New game coming up...")
                        self.log_system_message("All players have been eliminated. New game coming up...")
                        self.players.update(self.eliminated)
                        self.restart_game()

                    elif(len(self.players) == 1): #only one player remains, making him the automatic winner
                        if(player_name in self.players):
                            self.broadcast_game(f"{player_name} has won the game! New game coming up...")
                            self.log_system_message(f"{player_name} has won the game! New game coming up...")

                            self.players.update(self.eliminated)
                            time.sleep(0.1)
                            self.update_players_list_after_game(player_name)
                            time.sleep(0.1)
                            self.restart_game()

                    else:
                        result = self.evaluate_results()
                        how_many_winners = sum(1 for value in self.choices.values() if value == result)

                        self.broadcast_all(("CHOICES:\n" + str(self.choices))) #display everyones choices
                        time.sleep(0.1)
                    
                        if how_many_winners == 1: #the game is over if there is a single winner, restart game
                            for key, value in self.choices.items():
                                if value == result:
                                    winner_name = key
                            if player_name == winner_name:
                                client_socket.send("YOU WON!".encode("utf-8"))
                                self.broadcast_game(f"{winner_name} has won the game! New game coming up...")
                                self.log_system_message(f"{winner_name} has won the game! New game coming up...")

                                self.players.update(self.eliminated) #add the eliminated players back to players dict
                                time.sleep(0.1)
                                self.update_players_list_after_game(winner_name)
                                time.sleep(0.1)
                                self.restart_game()

                        elif result == "TIE":
                            if player_name in self.players:
                                client_socket.send("IT WAS A TIE. New Round Go!".encode("utf-8"))
                                    
                        elif player_choice != result:
                            if player_name in self.players:
                                self.eliminated[player_name] = client_socket #eliminate player if lost
                                del self.players[player_name]
                                client_socket.send("YOU LOST. Spectate.".encode("utf-8")) 

                        elif player_choice == result and player_name in self.players:
                            client_socket.send("YOU GO TO THE NEXT ROUND. New Round, Go!".encode("utf-8"))
                            

            except socket.error:  #client disconnects
                if name in self.players.keys():
                    del self.players[name]
                    self.update_players_list()
                    self.log_system_message(f"{name} disconnected.")
                    self.broadcast(f"{name} disconnected.")

                elif name in self.queue.values():
                    del self.queue[name]
                    self.queue_order.remove(name)
                    self.log_system_message(f"{name} disconnected.")
                    self.log_system_message(f"{name} disconnected.")

                elif name in self.eliminated.keys():
                    del self.eliminated[name]
                    self.log_system_message(f"{name} disconnected from game.")
                    self.broadcast(f"{name} disconnected from game.")

                client_socket.close()

            except Exception as e:
                if name in self.players.keys():
                    del self.players[name]
                    self.update_players_list()
                    self.log_system_message(f"{name} disconnected.")
                    self.broadcast(f"{name} disconnected.")

                elif name in self.queue.values():
                    del self.queue[name]
                    self.queue_order.remove(name)
                    self.log_system_message(f"{name} disconnected.")
                    self.broadcast(f"{name} disconnected.")

                elif name in self.eliminated.keys():
                    del self.eliminated[name]
                    self.log_system_message(f"{name} disconnected from game.")
                    self.broadcast(f"{name} disconnected from game.")

                client_socket.close()
                self.log_system_message(f"An error occurred: {e}")
                break

    def start_server(self):  #start the server
        port = int(self.port_entry.get())

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IP address and port configurations
        server_socket.bind(("", port))
        server_socket.listen()
        self.log_system_message(f"Server listening on port {port}.")

        def accept_connections():
            while True:
                client_socket, address = server_socket.accept()
                threading.Thread(
                    target=self.handle_client, args=(client_socket, address)
                ).start()

        threading.Thread(target=accept_connections, daemon=True).start() #start thread


root = tk.Tk()
app = ServerApp(root)
root.mainloop()
