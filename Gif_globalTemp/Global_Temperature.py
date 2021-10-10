#!/usr/bin/env python
# coding: utf-8

# # 简单的全球温度动态图
# 作者：邓楠 
# dengnan987@gmail.com

# ## 导入包

# In[3]:


import numpy as np 
import xarray as xr
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


# ## ECMWF的api脚本，一次一个
# 
# > import cdsapi
# >
# >c = cdsapi.Client()
# >
# >c.retrieve(
#     'reanalysis-era5-pressure-levels',
#     {
#         'product_type': 'reanalysis',
#         'variable': 'temperature',
#         'pressure_level': '1000',
#         'year': '1998',
#         'month': '06',
#         'day': '08',
#         'time': [
#             '08:00', '10:00', '12:00',
#             '14:00', '16:00', '18:00',
#         ],
#         'format': 'netcdf',
#     },
#     'download.nc')
#     
#  * 批量下载可写另外的脚本，见csdn[孤城_001](https://blog.csdn.net/u011620268/article/details/97560996?utm_medium=distribute.pc_relevant_download.none-task-blog-blogcommendfrombaidu-2.nonecase&depth_1-utm_source=distribute.pc_relevant_download.none-task-blog-blogcommendfrombaidu-2.nonecas)

# In[4]:


import os
rootdir = './'  #数据的文件夹
list = os.listdir(rootdir)   #把所有文件的名字读入到list里
list


# In[7]:


ds = xr.open_dataset(rootdir+list[1],decode_times=False)
temp = ds.t-273.15  # 将K转换摄氏度温度
ds.t.shape


# In[8]:


ds


# ## 看每个纬度的最大温度值为多少

# In[11]:


a = temp[1,:,:].max(axis=1)
a


# ## 画图

# In[6]:


# 创建画图空间
proj = ccrs.PlateCarree(central_longitude=180)  #创建投影
fig = plt.figure(figsize=(12,8))  #创建页面
ax = fig.subplots(1, 1, subplot_kw={'projection': proj})  #子图
# 设置地图属性:加载国界、海岸线
ax.add_feature(cfeat.BORDERS.with_scale('110m'), linewidth=0.8, zorder=1) # The Resolution for world suggested to be 110
ax.add_feature(cfeat.COASTLINE.with_scale('110m'), linewidth=0.6, zorder=1)  
# 标注坐标轴
ax.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
#网格点属性
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
    linewidth=1.2, color='k', alpha=0.5, linestyle='--')
gl.xlabels_top = False #关闭顶端标签
gl.ylabels_right = False #关闭右侧标签
gl.xlabels_bottom = False
gl.ylabels_left = False
# zero_direction_label用来设置经度的0度加不加E和W
lon_formatter = LongitudeFormatter(zero_direction_label=False)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
# 设置colorbar
cbar_kwargs = {
   'orientation': 'vertical',
   'label': 'temperature (℃)',
   'shrink': 0.6,
   'ticks': np.arange(-35,39,7)
}
levels = np.arange(-5,35,5)
temp[0,:,:].plot.contourf(ax=ax, levels=levels, cmap='Spectral_r', 
    cbar_kwargs=cbar_kwargs, transform=ccrs.PlateCarree())
ax.set_title("Global Temperature on June 8, 1998")  # Add a title to the axes.
plt.xlabel(None)
plt.ylabel(None)

#fig.show()
plt.savefig('temp{i}.png')


# ## 循环画图

# In[16]:


image_list=[]

for i in range(6):
    proj = ccrs.PlateCarree(central_longitude=180)  #创建投影
    fig = plt.figure(figsize=(12,8))  #创建页面
    ax = fig.subplots(1, 1, subplot_kw={'projection': proj})  #子图
    # 设置地图属性:加载国界、海岸线
    ax.add_feature(cfeat.BORDERS.with_scale('110m'), linewidth=0.8, zorder=1) # The Resolution for world suggested to be 110
    ax.add_feature(cfeat.COASTLINE.with_scale('110m'), linewidth=0.6, zorder=1)  
    # 标注坐标轴
    ax.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
    ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
    #网格点属性
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
        linewidth=1.2, color='k', alpha=0.5, linestyle='--')
    gl.xlabels_top = False #关闭顶端标签
    gl.ylabels_right = False #关闭右侧标签
    gl.xlabels_bottom = False
    gl.ylabels_left = False
    # zero_direction_label用来设置经度的0度加不加E和W
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    # 设置colorbar
    cbar_kwargs = {
       'orientation': 'vertical',
       'label': 'temperature (℃)',
       'shrink': 0.6,
       'ticks': np.arange(-35,39,7)
    }
    levels = np.arange(-5,35,5)
    temp[i,:,:].plot.contourf(ax=ax, levels=levels, cmap='Spectral_r', 
                              cbar_kwargs=cbar_kwargs, transform=ccrs.PlateCarree())
    ax.set_title('Global Temperature on {}:00 June 8, 1998'.format(2*i+8))  # Add a title to the axes.
    plt.xlabel(None)
    plt.ylabel(None)

    #fig.show()
    image_list.append('temp{}.png'.format(i))
    plt.savefig('temp{}.png'.format(i))


# ## 6张图片转gif

# In[37]:


import imageio


# In[38]:


def create_gif(image_list, gif_name, duration=0.35):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return

def main():
    #image_list = []
    gif_name = 'temp.gif'
    duration = 0.35
    create_gif(image_list, gif_name, duration)


# In[39]:


if __name__ == '__main__':
    main()


# ## 蟹蟹 
