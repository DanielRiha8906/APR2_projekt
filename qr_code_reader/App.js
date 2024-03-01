import { Text, Button, Input, theme, Block } from "galio-framework";
import React, { useState, useEffect} from "react";
import { StyleSheet, View } from "react-native";
import { Camera } from "expo-camera";
//Nezapomenou změnit IP -> ipconfig
const url = "http://192.168.86.88:5000/guide"

//
export default function App() {
  //
  const [hasPermission, setHasPermission] = useState(null);
  const [user, setUser] = useState("")
  const [text, setText] = useState("")
  const [status, setStatus] = useState(0) // 200 - 402 - 417
  const [scanned, setScanned] = useState(true);
  // vyžádání permisí na kameru v androidu
  async function Permission() {
    const { status } = await Camera.requestCameraPermissionsAsync();
    setHasPermission(status === "granted");
  }
//Lambda asynchronní funkce ktera se runne na začátku renderování, prázdný array kvůli dependabilities
  useEffect(() => {
    Permission()
  }, []);

//asynchronní funkce -> místo async a await se používá .then (počká se, až se to dojede, pak se to spustí)
  const handleBarCodeScanned = ({ data }) => {
    setScanned(true);

    fetch(url, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user: user,
        qr_code: data,
      }),
    }).then(response => {
      setStatus(response.status)
    })
  };


  const renderCamera = () => {
    return (
      <View style={styles.cameraContainer}>
        <Camera
          onBarCodeScanned={handleBarCodeScanned}
          style={styles.camera}
        />
      </View>
    );
  };


//Login screen, user input + mám button, ty žijou sami -> potřebuji proměnné házet do use statu abych to mohl vytáhnout (V moment stisku tlačítka to recordne, kdyŽ se to potom změní tak smůla)
  if(user === "") {
    return <View style={styles.container}>
      <Text h4> Insert username </Text>
      <Input placeholder="stxxxxx" color={theme.COLORS.INFO} style={{ borderColor: theme.COLORS.INFO }} placeholderTextColor={theme.COLORS.INFO} onChangeText={(e) => setText(e)}/>
      <Button onPress={() => {
        setUser(text)
      }}> Login </Button>
    </View>
  }

//Fatální error -> useEffect když nefunguje -> Edge case fix
  if (hasPermission === null) {
    return <View />;
  }
// Pokuď nemám permice na kameru -> vypíše mi, že nemám skrz galio framework, vytvoří se button na kliknutí a přidání rights
  if (hasPermission === false) {
    return (
      <View style={styles.container}>
        <Text h3>Rights not found </Text>
        <Text>This application requires camera permissions  </Text>
        <Button onPress={() => Permission()}>Add camera rights </Button>
      </View>
    );
  }
//Velkej if - když 0 - žádný response, když 200 success jinak error
  return (
    <View style={styles.container}>
      {status != 0?
        status == 402?
          <Block card>
            <Text style={{ color: theme.COLORS.WARNING }}  h5> QR has been used </Text>
          </Block> :
        status == 200?
        <Block card>
            <Text style={{ color: theme.COLORS.SUCCESS}}  h5> Succes ! </Text>
          </Block> :
          <Block card>
            <Text style={{ color: theme.COLORS.DRIBBBLE }}  h5> Wrong QR code ! </Text>
          </Block>

      : null
      }
      <Text h3>UJEP Scanner </Text>
      {scanned ? <View style={styles.cameraContainer}/> : renderCamera()}
      {scanned ? (
        <Button color="success" round size="large" onPress={() => setScanned(false)}>Start scanning </Button>
      ) : (
        <Button color="#FF5733" round size="large" onPress={() => setScanned(true)}>Stop scanning </Button>
      )}
    </View>
  );
}
//
const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  cameraContainer: {
    width: "80%",
    aspectRatio: 1,
    overflow: "hidden",
    borderRadius: 10,
    marginBottom: 40,
  },
  camera: {
    flex: 1,
  },
});
