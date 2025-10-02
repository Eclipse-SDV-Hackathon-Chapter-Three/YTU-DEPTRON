/* 
 * Copyright (c) Microsoft
 * Copyright (c) 2024 Eclipse Foundation
 * 
 *  This program and the accompanying materials are made available 
 *  under the terms of the MIT license which is available at
 *  https://opensource.org/license/mit.
 * 
 *  SPDX-License-Identifier: MIT
 * 
 *  Contributors: 
 *     Microsoft         - Initial version
 *     Frédéric Desbiens - 2024 version.
 */

#ifndef _CLOUD_CONFIG_H
#define _CLOUD_CONFIG_H

typedef enum
{
    None         = 0,
    WEP          = 1,
    WPA_PSK_TKIP = 2,
    WPA2_PSK_AES = 3
} WiFi_Mode;

// ----------------------------------------------------------------------------
// WiFi connection config
// ----------------------------------------------------------------------------
#define HOSTNAME      "etxdkc3t1"  
#define WIFI_SSID     "SDV_Chapter3-Team1"
#define WIFI_PASSWORD "EclipseSDVC3" 
#define WIFI_MODE     WPA2_PSK_AES
#define MQTTSRVIP1  192
#define MQTTSRVIP2  168
#define MQTTSRVIP3  89
#define MQTTSRVIP4  249

//#define NETWORK_INIT_SNTP 

// ----------------------------------------------------------------------------
// MQTT Config
// ----------------------------------------------------------------------------


#endif // _CLOUD_CONFIG_H
