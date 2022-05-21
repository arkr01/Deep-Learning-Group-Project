#%%

import torch
import pandas as pd
import numpy as np

#%%

BBB_filepath = "C:/Users/lachl/Google Drive/Uni Year 5/git_stuff/STAT3007Project/csv_files/cricsheet_data_partial.csv"

# %%
def read_data(filepath=BBB_filepath):
    df = pd.read_csv(filepath)
    return df

def get_bowler_one_hot(df):
    bowler_columns = [col_name for col_name in df.columns if "bowler" in col_name]

    bowler_df = df[bowler_columns]

    # todo - return these probably 
    # name_to_one_hot = 
    # one_hot_to_name = 
    one_hot_numpy = df[bowler_columns[2:]].to_numpy()

    return torch.FloatTensor(one_hot_numpy)

def get_batsman_one_hot(df):
    batsman_columns = [col_name for col_name in df.columns if "batter" in col_name]

    batsman_df = df[batsman_columns]

    # todo - return these probably 
    # name_to_one_hot = 
    # one_hot_to_name = 
    
    one_hot_numpy = df[batsman_columns[3:]].to_numpy()

    return torch.FloatTensor(one_hot_numpy)

def get_result_tens(df):
    #blahh
    ret_val = df[["wicket_kind", "t_runs_0", "t_runs_1", "t_runs_2", "t_runs_3", "t_runs_4", "t_runs_5", "t_runs_6"]]
    extra_one_hot = [i for i in ret_val["wicket_kind"].unique() if isinstance(i, str)]

    for wicket_title in extra_one_hot:
        ret_val[wicket_title] = 1 * (ret_val["wicket_kind"] == wicket_title)

    return torch.FloatTensor(ret_val.iloc[:,1:].to_numpy())

def get_ground_tens(df):
    venue_col = [head for head in df.columns if "v_" in head]
    return df[venue_col].to_numpy()

def ID_to_batter(df, ID):
    batsman_columns = [col_name for col_name in df.columns if "batter" in col_name]
    batsman_df = df[batsman_columns]
    return df[batsman_columns]


df = read_data()
batters = get_batsman_one_hot(df)
bowlers = get_bowler_one_hot(df)
results = get_result_tens(df)
ground = get_ground_tens(df)


print(bowlers.shape, batters.shape, results.shape)

#%%
class Embed_Model(torch.nn.Module):
        def __init__(self, num_batsman, batsman_embed_dim, num_bowlers, bowler_embed_dim, pred_size=11):
            super(Embed_Model, self).__init__()

            self.num_batsman = num_batsman
            self.num_bowlers = num_bowlers

            self.batsman_embed = torch.nn.Linear(self.num_batsman, batsman_embed_dim)
            self.bowler_embed = torch.nn.Linear(self.num_bowlers, bowler_embed_dim)
            
            self.embed_to_res = torch.nn.Linear(batsman_embed_dim + bowler_embed_dim, pred_size)

            self.relu = torch.nn.ReLU()
            self.sigmoid = torch.nn.Sigmoid()

        def forward(self, batters, bowlers):
            bat_embed = self.batsman_embed(batters)
            bowl_embed = self.bowler_embed(bowlers)
            
            embed_space = torch.cat((bat_embed, bowl_embed), 1)

            return self.sigmoid(self.embed_to_res(embed_space))

        def get_batsman_embed(self, batters):
            return self.batsman_embed(batters)

        def get_bowler_embed(self, bowlers):
            return self.bowler_embed(bowlers)




# #%%
# model = Embed_Model(batters.shape[1], 10,  batters.shape[1], 10)
# criterion = torch.nn.BCELoss()
# optimizer = torch.optim.SGD(model.parameters(), lr = 0.1)

# model(batters, bowlers).shape

# #%%
# model.train()
# epoch = 100
# for epoch in range(epoch):
#     optimizer.zero_grad()
#     # Forward pass
#     y_pred = model(batters, bowlers)
#     # Compute Loss
#     loss = criterion(y_pred.squeeze(), results)
   
#     print('Epoch {}: train loss: {}'.format(epoch, loss.item()))
#     # Backward pass
#     loss.backward()
#     optimizer.step()



#%%
def get_embeddings(embedding_filename = "", raw_data_file_name= "", batter_embed_size =10, bowler_embed_size=10, num_it = 500):
    
    if embedding_filename == "":
        # calculate embeddings normally

        df = read_data()
        batters = get_batsman_one_hot(df)
        bowlers = get_bowler_one_hot(df)
        results = get_result_tens(df)

        model = Embed_Model(batters.shape[1], batter_embed_size,  batters.shape[1], batter_embed_size, results.shape[1])
        criterion = torch.nn.BCELoss()
        optimizer = torch.optim.SGD(model.parameters(), lr = 0.2)

        model.train()
        epoch = num_it

        for epoch in range(epoch):
            optimizer.zero_grad()
            # Forward pass
            y_pred = model(batters, bowlers)
            # Compute Loss
            loss = criterion(y_pred.squeeze(), results)
        
            print('Epoch {}: train loss: {}'.format(epoch, loss.item()))
            # Backward pass
            loss.backward()
            optimizer.step()
        
        # write file 

        return model.get_batsman_embed(batters), model.get_bowler_embed(bowlers), model, results, get_ground_tens(df), df

    else:
        # read file
        pass

#bat_at_ball, bowl_at_ball, model, results, pitch= get_embeddings(raw_data_file_name=BBB_filepath)

# print(a.shape, b.shape, c.shape)
# # %%

# num_batsman = len(df["batter_name"].unique())
# num_bowlers = len(df["bowler_name"].unique())
# num_batsman
# # all_batsman = model.get_batsman_embed(torch.eye(165))
# # all_bowlers = model.get_bowler_embed(torch.eye(165))

# #%%
# # plot embeddings of players 
# from sklearn.decomposition import PCA
# import seaborn as sns

# pca = PCA(n_components=2)

# pca.fit(all_batsman.detach().numpy())

# plot_vals = pca.fit_transform(all_batsman.detach().numpy())

# sns.scatterplot(x=plot_vals[:, 0], y=plot_vals[:, 1])


# #%%

# # from sklearn.decomposition import PCA
# # import seaborn as sns

# # pca = PCA(n_components=2)

# # pca.fit(all_bowlers.detach().numpy())

# # plot_vals = pca.fit_transform(all_bowlers.detach().numpy())

# # sns.scatterplot(x=plot_vals[:, 0], y=plot_vals[:, 1])

# %%
